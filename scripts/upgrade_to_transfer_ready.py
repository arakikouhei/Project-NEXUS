from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / datetime.now().strftime("transfer_%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return

    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        shutil.copy2(path, target)


def write_file(path_text: str, content: str) -> None:
    path = ROOT / path_text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def append_gitignore() -> None:
    path = ROOT / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    additions = [
        "__pycache__/",
        "*.pyc",
        ".DS_Store",
        "logs/",
        "*.log",
        "backups/",
        "exports/",
        "data/worklog.json",
    ]

    lines = existing.splitlines()
    changed = False

    for item in additions:
        if item not in lines:
            lines.append(item)
            changed = True

    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in [
        ".gitignore",
        "nexus/tools/manager.py",
        "scripts/integration_check.py",
    ]:
        backup(file_path)

    write_file(
        "nexus/transfer/__init__.py",
        '''
        """
        Project NEXUS
        Transfer package
        """
        ''',
    )

    write_file(
        "nexus/transfer/exporter.py",
        r'''
        """
        Project NEXUS
        Sphere Transfer Exporter
        """

        from __future__ import annotations

        from datetime import datetime
        import hashlib
        import json
        from pathlib import Path
        import shutil


        class SphereTransferExporter:
            """Creates a transfer package for future sphere hardware."""

            def __init__(self) -> None:
                self.root = Path.cwd()
                self.export_root = self.root / "exports"

                self.include_files = [
                    "README.md",
                    "CHANGELOG.md",
                    "requirements.txt",
                    "NEXUS_MANIFEST.md",
                    "main.py",
                    "console.py",
                    "config/settings.py",
                    "prompts/system_prompt.txt",
                    "data/memory.json",
                    "data/worklog.json",
                    "docs/ROADMAP.md",
                    "docs/PRE_SPHERE_PLAN.md",
                    "docs/SPHERE_TRANSFER.md",
                ]

                self.include_dirs = [
                    "nexus",
                    "config",
                    "prompts",
                    "docs",
                    "scripts",
                ]

                self.ignore_names = {
                    "__pycache__",
                    ".git",
                    ".venv",
                    "venv",
                    ".DS_Store",
                    "backups",
                    "exports",
                    "logs",
                }

                self.ignore_suffixes = {
                    ".pyc",
                    ".pyo",
                    ".log",
                }

            def preview(self) -> str:
                files = self._existing_files()
                dirs = self._existing_dirs()

                lines = [
                    "## Sphere Transfer Preview",
                    "",
                    "このパッケージには、将来球体側へ移すためのNEXUS本体・設定・記憶データが含まれます。",
                    "",
                    "### Files",
                ]

                if files:
                    for file_path in files:
                        lines.append(f"- {file_path}")
                else:
                    lines.append("- なし")

                lines.append("")
                lines.append("### Directories")

                if dirs:
                    for dir_path in dirs:
                        lines.append(f"- {dir_path}/")
                else:
                    lines.append("- なし")

                lines.append("")
                lines.append("### Excluded")
                lines.append("- .git/")
                lines.append("- __pycache__/")
                lines.append("- logs/")
                lines.append("- backups/")
                lines.append("- exports/")
                lines.append("")
                lines.append("作成する場合は `移行パッケージ作成` と入力してください。")

                return "\n".join(lines)

            def create_package(self) -> dict:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                package_name = f"sphere_transfer_{timestamp}"
                package_dir = self.export_root / package_name

                package_dir.mkdir(parents=True, exist_ok=True)

                copied_files = []
                copied_dirs = []

                for file_text in self._existing_files():
                    src = self.root / file_text
                    dst = package_dir / file_text
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    copied_files.append(file_text)

                for dir_text in self._existing_dirs():
                    src = self.root / dir_text
                    dst = package_dir / dir_text

                    if dst.exists():
                        shutil.rmtree(dst)

                    shutil.copytree(
                        src,
                        dst,
                        ignore=self._ignore_for_copy,
                    )
                    copied_dirs.append(dir_text)

                manifest = {
                    "name": package_name,
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                    "project": "Project NEXUS",
                    "stage": "Sphere Transfer Ready",
                    "purpose": "Transfer NEXUS software, settings, prompts, docs, and memory data to future sphere hardware.",
                    "copied_files": copied_files,
                    "copied_directories": copied_dirs,
                    "excluded": sorted(self.ignore_names),
                    "notes": [
                        "This package does not enable real hardware control.",
                        "Use this package when preparing a future sphere-side environment.",
                        "Logs, backups, git data, and caches are intentionally excluded.",
                    ],
                }

                manifest_path = package_dir / "TRANSFER_MANIFEST.json"
                manifest_path.write_text(
                    json.dumps(manifest, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

                readme_path = package_dir / "TRANSFER_README.md"
                readme_path.write_text(self._transfer_readme(), encoding="utf-8")

                archive_base = self.export_root / package_name
                archive_path = shutil.make_archive(
                    str(archive_base),
                    "zip",
                    root_dir=self.export_root,
                    base_dir=package_name,
                )

                checksum = self._sha256(Path(archive_path))

                checksum_path = Path(archive_path).with_suffix(".sha256.txt")
                checksum_path.write_text(
                    f"{checksum}  {Path(archive_path).name}\n",
                    encoding="utf-8",
                )

                return {
                    "package_dir": str(package_dir),
                    "archive_path": str(archive_path),
                    "checksum": checksum,
                }

            def _existing_files(self) -> list[str]:
                return [
                    file_text
                    for file_text in self.include_files
                    if (self.root / file_text).exists()
                ]

            def _existing_dirs(self) -> list[str]:
                return [
                    dir_text
                    for dir_text in self.include_dirs
                    if (self.root / dir_text).exists()
                ]

            def _ignore_for_copy(self, directory: str, names: list[str]) -> set[str]:
                ignored = set()

                for name in names:
                    path = Path(name)

                    if name in self.ignore_names:
                        ignored.add(name)
                        continue

                    if path.suffix in self.ignore_suffixes:
                        ignored.add(name)

                return ignored

            def _transfer_readme(self) -> str:
                return """# Project NEXUS Sphere Transfer Package

        This package contains a transferable snapshot of Project NEXUS.

        It is intended for preparing a future sphere-side environment.

        ## Included

        - NEXUS source code
        - Configuration
        - Prompts
        - Documentation
        - Memory data if available
        - Work log data if available

        ## Not Included

        - Git history
        - Logs
        - Backups
        - Python cache files
        - Real hardware drivers

        ## Important

        This package does not activate physical hardware control.

        Before moving to real sphere hardware, add:

        - Safety Core
        - Permission checks
        - Emergency stop
        - Hardware bridge
        - Device logs
        - Manual override
        """

            def _sha256(self, path: Path) -> str:
                digest = hashlib.sha256()

                with path.open("rb") as file:
                    for chunk in iter(lambda: file.read(1024 * 1024), b""):
                        digest.update(chunk)

                return digest.hexdigest()
        ''',
    )

    write_file(
        "nexus/tools/transfer.py",
        r'''
        """
        Project NEXUS
        Transfer Tool
        """

        from nexus.tools.base_tool import BaseTool
        from nexus.transfer.exporter import SphereTransferExporter


        class TransferTool(BaseTool):
            """Creates transfer packages for future sphere hardware."""

            name = "transfer"
            description = "球体側へ移すための移行パッケージを作成します"

            def __init__(self) -> None:
                self.exporter = SphereTransferExporter()

            def can_handle(self, user_input: str) -> bool:
                keywords = {
                    "移行内容確認",
                    "移行パッケージ作成",
                    "球体移行",
                    "球体へ移す",
                    "転送パッケージ",
                    "transfer package",
                }
                return any(keyword in user_input for keyword in keywords)

            def execute(self, user_input: str) -> str:
                if "移行内容確認" in user_input:
                    return self.exporter.preview()

                if (
                    "移行パッケージ作成" in user_input
                    or "球体移行" in user_input
                    or "球体へ移す" in user_input
                    or "転送パッケージ" in user_input
                    or "transfer package" in user_input
                ):
                    result = self.exporter.create_package()

                    return (
                        "## Sphere Transfer Package Created\n\n"
                        f"Folder: {result['package_dir']}\n"
                        f"Zip: {result['archive_path']}\n"
                        f"SHA256: {result['checksum']}\n\n"
                        "このzipを将来の球体側環境へ移せば、NEXUSのソフト・設定・記憶データを復元する準備ができます。"
                    )

                return "対応していない移行操作です。"
        ''',
    )

    write_file(
        "docs/SPHERE_TRANSFER.md",
        r'''
        # Project NEXUS Sphere Transfer Guide

        This document explains how to prepare NEXUS data for a future sphere-side environment.

        ## Goal

        The current goal is not to control real sphere hardware yet.

        The goal is to make NEXUS transferable at any time.

        ## Transfer Package

        Use this command inside NEXUS:

        ```text
        移行パッケージ作成
        ```

        NEXUS will create:

        ```text
        exports/sphere_transfer_YYYYMMDD_HHMMSS.zip
        ```

        ## Included Data

        - Source code
        - Configuration
        - Prompts
        - Documentation
        - Memory data
        - Work log data

        ## Excluded Data

        - Git history
        - Logs
        - Backups
        - Python cache files

        ## Next Stage

        After the physical sphere hardware is ready, this transfer package can be moved to the sphere-side environment.

        Real hardware control should only be enabled after Safety Core is implemented.
        ''',
    )

    write_file(
        "nexus/tools/manager.py",
        r'''
        """
        Project NEXUS
        Tool Manager
        """

        from nexus.tools.base_tool import BaseTool
        from nexus.tools.clock import ClockTool
        from nexus.tools.git import GitTool
        from nexus.tools.terminal import TerminalTool
        from nexus.tools.context import ContextTool
        from nexus.tools.system import SystemTool
        from nexus.tools.voice import VoiceTool
        from nexus.tools.test import TestTool
        from nexus.tools.dashboard import DashboardTool
        from nexus.tools.worklog import WorkLogTool
        from nexus.tools.hardware import HardwareTool
        from nexus.tools.capability import CapabilityTool
        from nexus.tools.transfer import TransferTool
        from nexus.tools.calculator import CalculatorTool
        from nexus.tools.filesystem import FileSystemTool
        from nexus.tools.project import ProjectTool
        from nexus.tools.code import CodeTool


        class ToolManager:
            """Manages all tools."""

            def __init__(self) -> None:
                self.tools: list[BaseTool] = []

                self.register(ClockTool())
                self.register(GitTool())
                self.register(TerminalTool())
                self.register(ContextTool())
                self.register(SystemTool())
                self.register(VoiceTool())
                self.register(TestTool())
                self.register(DashboardTool())
                self.register(WorkLogTool())
                self.register(HardwareTool())
                self.register(CapabilityTool())
                self.register(TransferTool())
                self.register(CalculatorTool())
                self.register(FileSystemTool())
                self.register(ProjectTool())
                self.register(CodeTool())

            def register(self, tool: BaseTool) -> None:
                self.tools.append(tool)

            def execute(self, user_input: str) -> str | None:
                for tool in self.tools:
                    if tool.can_handle(user_input):
                        return tool.execute(user_input)

                return None
        ''',
    )

    append_gitignore()

    print("Sphere Transfer Ready files written.")
    print(f"Backup saved to: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
