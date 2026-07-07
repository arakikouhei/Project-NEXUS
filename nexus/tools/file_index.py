from pathlib import Path
from typing import Dict, List, Tuple

class FileIndexTool:
    """Read-only project file index tool."""

    IMPORTANT_DIRS = [
        "docs",
        "nexus",
        "nexus/tools",
        "nexus/agent",
        "scripts",
        "prompts",
        "data",
        "data/project",
        "data/knowledge",
        "data/work_notes",
    ]

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        "backups",
    }

    IMPORTANT_SUFFIXES = {
        ".py",
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
    }

    COMMANDS = {
        "ファイルインデックス",
        "重要ファイル一覧",
        "docs一覧",
        "data一覧",
        "tools一覧",
        "scripts一覧",
        "prompts一覧",
    }

    def can_handle(self, text: str) -> bool:
        text = text.strip()
        return text in self.COMMANDS

    def execute(self, text: str) -> str:
        return self.handle(text)

    def handle(self, text: str) -> str:
        text = text.strip()

        if text == "ファイルインデックス":
            return self._project_overview()

        if text == "重要ファイル一覧":
            return self._important_files()

        if text == "docs一覧":
            return self._directory_listing("docs")

        if text == "data一覧":
            return self._directory_listing("data")

        if text == "tools一覧":
            return self._directory_listing("nexus/tools")

        if text == "scripts一覧":
            return self._directory_listing("scripts")

        if text == "prompts一覧":
            return self._directory_listing("prompts")

        return "File Index: unsupported command."

    def _project_overview(self) -> str:
        lines = [
            "## File Index",
            "",
            "Project NEXUS file overview.",
            "",
            "### Important Directories",
        ]

        for directory in self.IMPORTANT_DIRS:
            path = Path(directory)
            status = "exists" if path.exists() else "missing"
            file_count = self._count_files(path) if path.exists() else 0
            lines.append(f"- `{directory}`: {status}, files={file_count}")

        lines += [
            "",
            "### Available Commands",
            "- ファイルインデックス",
            "- 重要ファイル一覧",
            "- docs一覧",
            "- data一覧",
            "- tools一覧",
            "- scripts一覧",
            "- prompts一覧",
            "",
            "Safety: read-only. This tool does not edit or delete files.",
        ]

        return "\n".join(lines)

    def _important_files(self) -> str:
        files = self._collect_important_files(limit=120)

        lines = [
            "## File Index",
            "",
            "Important project files.",
            "",
        ]

        if not files:
            lines.append("No important files found.")
            return "\n".join(lines)

        grouped: Dict[str, List[str]] = {}
        for path in files:
            top = path.parts[0] if path.parts else "."
            grouped.setdefault(top, []).append(path.as_posix())

        for group in sorted(grouped):
            lines.append(f"### {group}")
            for item in grouped[group][:30]:
                lines.append(f"- `{item}`")
            if len(grouped[group]) > 30:
                lines.append(f"- ... and {len(grouped[group]) - 30} more")
            lines.append("")

        return "\n".join(lines).rstrip()

    def _directory_listing(self, directory: str) -> str:
        path = Path(directory)

        lines = [
            "## File Index",
            "",
            f"Directory: `{directory}`",
            "",
        ]

        if not path.exists():
            lines.append("Status: missing")
            return "\n".join(lines)

        if not path.is_dir():
            lines.append("Status: not a directory")
            return "\n".join(lines)

        entries = self._list_directory(path)

        if not entries:
            lines.append("No files found.")
            return "\n".join(lines)

        lines.append("### Entries")
        for label, rel_path in entries[:80]:
            lines.append(f"- {label} `{rel_path}`")

        if len(entries) > 80:
            lines.append(f"- ... and {len(entries) - 80} more")

        lines.append("")
        lines.append("Safety: read-only listing.")
        return "\n".join(lines)

    def _list_directory(self, path: Path) -> List[Tuple[str, str]]:
        entries: List[Tuple[str, str]] = []

        for child in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            if child.name in self.IGNORE_DIRS:
                continue

            label = "[dir]" if child.is_dir() else "[file]"
            entries.append((label, child.as_posix()))

        return entries

    def _collect_important_files(self, limit: int = 120) -> List[Path]:
        results: List[Path] = []

        roots = [
            Path("docs"),
            Path("nexus"),
            Path("scripts"),
            Path("prompts"),
            Path("data/project"),
            Path("data/work_notes"),
        ]

        for root in roots:
            if not root.exists():
                continue

            for path in root.rglob("*"):
                if len(results) >= limit:
                    return results

                if any(part in self.IGNORE_DIRS for part in path.parts):
                    continue

                if path.is_file() and path.suffix in self.IMPORTANT_SUFFIXES:
                    results.append(path)

        return sorted(results, key=lambda p: p.as_posix())

    def _count_files(self, path: Path) -> int:
        if not path.exists() or not path.is_dir():
            return 0

        count = 0
        for item in path.rglob("*"):
            if any(part in self.IGNORE_DIRS for part in item.parts):
                continue
            if item.is_file():
                count += 1
        return count
