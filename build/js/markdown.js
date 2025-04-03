document.addEventListener('DOMContentLoaded', async function () {
  // Dynamically import markdown-it
  const { default: MarkdownIt } = await import('markdown-it');

  // Import the core of highlight.js
  const { default: hljs } = await import('highlight.js/lib/core');

  // Register only the necessary languages
  const { default: html } = await import('highlight.js/lib/languages/xml');
  const { default: javascript } = await import('highlight.js/lib/languages/javascript');
  const { default: bash } = await import('highlight.js/lib/languages/bash');
  const { default: python } = await import('highlight.js/lib/languages/python');
  const { default: css } = await import('highlight.js/lib/languages/css');

  hljs.registerLanguage('html', html);  // Note: XML is used for HTML
  hljs.registerLanguage('javascript', javascript);
  hljs.registerLanguage('bash', bash);
  hljs.registerLanguage('python', python);
  hljs.registerLanguage('css', css);

  const editor = document.getElementById('editor');
  const preview = document.getElementById('preview');

  const md = new MarkdownIt({
    html: true,
    highlight: function (str, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(str, { language: lang }).value;
        } catch (__) { }
      }

      return ''; // use external default escaping
    }
  });

  function updatePreview() {
    const markdownText = editor.value;
    const html = md.render(markdownText);
    preview.innerHTML = html;
  }

  editor.addEventListener('input', updatePreview);
  updatePreview();

  // Toolbar Functions

  // Function to wrap selected text with formatting markers
  function applyInlineFormatting(marker) {
    // Get current selection
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const selectedText = editor.value.substring(start, end);

    // Only proceed if something is selected
    if (start !== end) {
      // Create formatted text by wrapping selection with markers
      const formattedText = `${marker}${selectedText}${marker}`;

      // Insert the formatted text
      editor.value =
        editor.value.substring(0, start) +
        formattedText +
        editor.value.substring(end);

      // Restore focus to the editor
      editor.focus();

      // Set selection to include the new formatting
      const markerLength = marker.length;
      editor.setSelectionRange(start + markerLength, end + markerLength);

      // Manually trigger update
      updatePreview();
    }
  }

  // Function to apply line-based formatting (headers, lists)
  function applyLineFormatting(prefix, ensureLineStart = true) {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const value = editor.value;

    // Find the start of the line where the cursor/selection begins
    let lineStart = start;
    while (lineStart > 0 && value[lineStart - 1] !== '\n') {
      lineStart--;
    }

    // Find all lines in the selection
    const selectedLines = value.substring(lineStart, end).split('\n');

    // Apply formatting to each line
    const formattedLines = selectedLines.map((line, index) => {
      // For the first line, consider the possibility that we're in the middle of a line
      if (index === 0 && !ensureLineStart) {
        return line;
      }

      // If line already has the prefix, don't add it again
      if (line.trimStart().startsWith(prefix.trimStart())) {
        return line;
      }

      // For numbered lists, we add the index + 1 to create sequential numbers
      if (prefix === '1. ' && index > 0) {
        return `${index + 1}. ${line.trimStart()}`;
      }

      return `${prefix}${line.trimStart()}`;
    });

    // Replace the text
    const replacement = formattedLines.join('\n');
    editor.value =
      value.substring(0, lineStart) +
      replacement +
      value.substring(end);

    // Restore cursor position
    editor.focus();
    const newEnd = lineStart + replacement.length;
    editor.setSelectionRange(newEnd, newEnd);

    // Manually trigger update
    updatePreview();
  }

  function insertLink() {
    const url = prompt('Enter the URL:', 'https://');
    if (!url) return;

    const selectionStart = editor.selectionStart;
    const selectionEnd = editor.selectionEnd;

    let selectedText = editor.value.substring(selectionStart, selectionEnd).trim();
    if (!selectedText) {
      selectedText = prompt('Enter the link text:');
    }

    if (selectedText) {
      const linkText = `[${selectedText}](${url})`;
      editor.value =
        editor.value.substring(0, selectionStart) +
        linkText +
        editor.value.substring(selectionEnd);

      editor.focus();
      const cursorPos = selectionStart + linkText.length;
      editor.setSelectionRange(cursorPos, cursorPos);

      // Manually trigger update
      updatePreview();
    }
  }

  // Buttons

  document.getElementById('copymarkdown-button').addEventListener('click', function () {
    navigator.clipboard.writeText(editor.value)
      .catch(err => console.error('Failed to copy text: ', err));
  });

  document.getElementById('copyhtml-button').addEventListener('click', function () {
    navigator.clipboard.writeText(preview.innerHTML)
      .catch(err => console.error('Failed to copy text: ', err));
  });

  document.getElementById('bold-button').addEventListener('click', () => {
    applyInlineFormatting('**');
  });

  document.getElementById('italic-button').addEventListener('click', () => {
    applyInlineFormatting('_');
  });

  document.getElementById('h1-button').addEventListener('click', () => {
    applyLineFormatting('# ');
  });

  document.getElementById('h2-button').addEventListener('click', () => {
    applyLineFormatting('## ');
  });

  document.getElementById('h3-button').addEventListener('click', () => {
    applyLineFormatting('### ');
  });

  document.getElementById('ul-button').addEventListener('click', () => {
    applyLineFormatting('- ');
  });

  document.getElementById('ol-button').addEventListener('click', () => {
    applyLineFormatting('1. ');
  });

  document.getElementById('link-button').addEventListener('click', insertLink);
});
