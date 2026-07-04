"""
Project NEXUS
Python Parser
"""

import ast
from pathlib import Path


class PythonParser:
    """Parses Python source files."""

    def parse(self, path: str | Path) -> ast.AST:
        """Parse a Python file into an AST."""

        path = Path(path)

        source = path.read_text(encoding="utf-8")

        return ast.parse(source)