"""
Project NEXUS
Code Index
"""

import ast
from pathlib import Path


class CodeIndex:
    """Indexes Python classes and functions."""

    def __init__(self, root: str = ".") -> None:
        self.root = Path(root)

    def search(self, keyword: str) -> list[str]:
        """Search Python definitions."""

        results = []

        for path in self.root.rglob("*.py"):

            if "__pycache__" in path.parts:
                continue

            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))

            except Exception:
                continue

            for node in ast.walk(tree):

                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):

                    if keyword.lower() in node.name.lower():

                        results.append(f"{path} : {node.name}")

        return results