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
