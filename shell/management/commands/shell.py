"""Python 3.13 REPL support using the unsupported _pyrepl module."""

from typing import ClassVar

from django.core.management.commands.shell import Command as BaseShellCommand


class Command(BaseShellCommand):
    """Custom shell command to support the pyrepl shell."""

    shells: ClassVar = ["ipython", "bpython", "pyrepl", "python"]

    def pyrepl(self, _) -> None:  # noqa: ANN001
        """Start a Python 3.13 REPL using the _pyrepl module."""
        from _pyrepl.main import interactive_console

        interactive_console()
