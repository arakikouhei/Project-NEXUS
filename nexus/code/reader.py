"""
Project NEXUS
Code Reader
"""

from pathlib import Path

from nexus.code.analyzer import CodeAnalyzer
from nexus.code.parser import PythonParser
from nexus.code.summary import CodeSummary


class CodeReader:
    """Reads and analyzes Python source files."""

    def __init__(self) -> None:
        self.parser = PythonParser()
        self.analyzer = CodeAnalyzer()
        self.summary = CodeSummary()

    def analyze_file(self, path: str | Path) -> str:
        """Analyze a Python file and return a summary."""

        tree = self.parser.parse(path)
        analysis = self.analyzer.analyze(tree)

        return self.summary.create(analysis)