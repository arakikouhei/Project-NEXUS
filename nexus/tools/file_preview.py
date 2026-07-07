from pathlib import Path


class FilePreviewTool:
    """Read-only safe text file preview tool."""

    COMMAND_PREFIXES = (
        "ファイル確認:",
        "docs確認:",
        "設定確認:",
    )

    ALLOWED_SUFFIXES = {
        ".py",
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".cfg",
    }

    BLOCKED_PARTS = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        "backups",
    }

    MAX_BYTES = 80_000
    MAX_LINES = 160

    def can_handle(self, text: str) -> bool:
        text = text.strip()
        return any(text.startswith(prefix) for prefix in self.COMMAND_PREFIXES)

    def execute(self, text: str) -> str:
        return self.handle(text)

    def handle(self, text: str) -> str:
        text = text.strip()

        if text.startswith("ファイル確認:"):
            raw_path = text.split(":", 1)[1].strip()
            return self._preview(raw_path)

        if text.startswith("docs確認:"):
            filename = text.split(":", 1)[1].strip()
            return self._preview(str(Path("docs") / filename))

        if text.startswith("設定確認:"):
            raw_path = text.split(":", 1)[1].strip()
            return self._preview(raw_path)

        return "File Preview: unsupported command."

    def _preview(self, raw_path: str) -> str:
        if not raw_path:
            return self._error("No path provided.")

        path = Path(raw_path).expanduser()

        safety_error = self._safety_check(path)
        if safety_error:
            return self._error(safety_error)

        if not path.exists():
            return self._error(f"File not found: `{raw_path}`")

        if not path.is_file():
            return self._error(f"Not a file: `{raw_path}`")

        if path.stat().st_size > self.MAX_BYTES:
            return self._error(
                f"File too large for preview: `{raw_path}` "
                f"({path.stat().st_size} bytes, limit {self.MAX_BYTES} bytes)"
            )

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return self._error("This file is not valid UTF-8 text.")
        except OSError as exc:
            return self._error(f"Could not read file: {exc}")

        lines = content.splitlines()
        shown = lines[: self.MAX_LINES]
        truncated = len(lines) > self.MAX_LINES

        output = [
            "## File Preview",
            "",
            f"Path: `{path.as_posix()}`",
            f"Size: {path.stat().st_size} bytes",
            f"Lines: {len(lines)}",
            "",
            "```text",
        ]

        output.extend(shown)
        output.append("```")

        if truncated:
            output += [
                "",
                f"Preview truncated: showing first {self.MAX_LINES} lines.",
            ]

        output += [
            "",
            "Safety: read-only preview. This tool does not edit or delete files.",
        ]

        return "\n".join(output)

    def _safety_check(self, path: Path) -> str:
        if path.is_absolute():
            try:
                project_root = Path.cwd().resolve()
                resolved = path.resolve()
                if project_root not in resolved.parents and resolved != project_root:
                    return "Absolute paths outside the project are blocked."
            except OSError:
                return "Could not safely resolve absolute path."

        parts = set(path.parts)
        blocked = parts.intersection(self.BLOCKED_PARTS)
        if blocked:
            return f"Blocked path part: `{sorted(blocked)[0]}`"

        if ".." in path.parts:
            return "Parent directory traversal is blocked."

        if path.suffix and path.suffix not in self.ALLOWED_SUFFIXES:
            return f"File suffix `{path.suffix}` is not allowed for preview."

        return ""

    def _error(self, message: str) -> str:
        return "\n".join(
            [
                "## File Preview",
                "",
                "Preview failed.",
                "",
                f"Reason: {message}",
                "",
                "Safety: read-only preview. This tool does not edit or delete files.",
            ]
        )
