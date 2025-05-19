"""Default Markdown Renderer."""

from importlib.util import find_spec

import mistune
from mistune.util import escape as escape_text
from mistune.util import safe_entity, striptags

# Check if Pygments is available
PYGMENTS_AVAILABLE = find_spec("pygments") is not None

if PYGMENTS_AVAILABLE:
    # Ignore Pylance for missing imports
    from pygments import highlight, lexers
    from pygments.formatters import html
    from pygments.util import ClassNotFound


class CustomRenderer(mistune.HTMLRenderer):
    """Custom renderer for Pygments syntax highlighting."""

    def __init__(self, *, escape: bool = False, **kwargs: dict) -> None:
        """Initialize the renderer."""
        super().__init__(**kwargs)

        if PYGMENTS_AVAILABLE:
            # create a cache for lexers to improve performance
            self._lexer_cache = {
                "example": lexers.TextLexer(),
            }
            self._formatter = html.HtmlFormatter()
            self._text_lexer = lexers.TextLexer()

        self._escape = escape
        self._mistune_escape = mistune.escape

    def block_code(self, code: str, info=None) -> str:  # noqa: ANN001
        """Override the code block renderer.

        Checks if Pygments is available and highlights the code block if possible.

        If Pygments is available, we override the default block_code method to highlight the code.

        Args:
            code (str): The code.
            info (any | None): The code info.

        Returns:
            any | str: The highlighted code block.
        """
        if PYGMENTS_AVAILABLE and info:
            # Clean and extract the language
            info = safe_entity(info.strip())

            if info:
                lang = info.split(None, 1)[0]

                # Get from cache or fallback to text lexer
                lexer = self._lexer_cache.get(lang.lower())

                if lexer is None:
                    try:
                        lexer = lexers.get_lexer_by_name(lang, stripall=True)

                        # Cache successful lexer lookups
                        self._lexer_cache[info.lower()] = lexer
                    except ClassNotFound:
                        # Fallback to text lexer if we can't find the lexer
                        lexer = self._text_lexer

                highlighted = highlight(code, lexer, self._formatter)
                return highlighted + "\n"

        # Fallback to basic code block
        html = "<pre><code"
        if info is not None:
            info = safe_entity(info.strip())
            if info:
                lang = info.split(None, 1)[0]
                html += ' class="language-' + lang + '"'
        return html + ">" + escape_text(code) + "</code></pre>\n"

    def image(self, text: str, url: str, title: str | None = None) -> str:
        """Override the image renderer.

        The default image renderer creates self-closing image tags which are no longer considered valid HTML. Instead
        we create a "void element" image tag which is valid HTML5.

        Args:
            text (str): The text.
            url (str): The URL.
            title (str | None): The title.

        Returns:
            str: The image tag.
        """
        src = self.safe_url(url)
        alt = escape_text(striptags(text))
        s = '<img src="' + src + '" alt="' + alt + '"'
        if title:
            s += ' title="' + safe_entity(title) + '"'
        return s + ">"

    def thematic_break(self) -> str:
        """Override the thematic break renderer.

        The default renderer creates a thematic break by using an HR tag. But the default renderer creates a
        self-closing HR tag which is no longer considered valid HTML. Instead we create a "void element" HR tag which is
        valid HTML5.

        Returns:
            str: The thematic break
        """
        return "<hr>\n"

    def linebreak(self) -> str:
        """Override the line break renderer.

        The default renderer creates a line break by using a BR tag. But the default renderer creates a self-closing BR
        tag which is no longer considered valid HTML. Instead we create a "void element" BR tag which is valid HTML5.

        Returns:
            str: The line break
        """
        return "<br>\n"


def mistune_renderer(markdown_text: str) -> str:
    """Render markdown text using Mistune.

    We use our custom rendered with the same defaults as the Mistune renderer.

    Args:
        markdown_text (str): The markdown text.

    Returns:
        str: The rendered markdown text.
    """
    renderer = CustomRenderer()
    markdown = mistune.create_markdown(
        escape=False,
        renderer=renderer,
        plugins=[
            "strikethrough",
            "table",
            "footnotes",
        ],
    )
    return markdown(markdown_text)
