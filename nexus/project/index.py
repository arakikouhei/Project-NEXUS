"""
Project NEXUS
Project Index
"""

from nexus.project.scanner import ProjectScanner


class ProjectIndex:
    """Searchable index of project files."""

    def __init__(self) -> None:
        self.scanner = ProjectScanner()
        self.files = self.scanner.scan()

    def refresh(self) -> None:
        """Refresh project file index."""
        self.files = self.scanner.scan()

    def search(self, keyword: str) -> list[str]:
        """Search files by keyword."""
        keyword = keyword.lower()

        return [
            file
            for file in self.files
            if keyword in file.lower()
        ]