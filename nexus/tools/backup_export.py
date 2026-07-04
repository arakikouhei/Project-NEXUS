"""
Project NEXUS
Backup / Export Tool v1

Creates local backups and exports for NEXUS knowledge data.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import shutil
import zipfile

from nexus.tools.base_tool import BaseTool


class BackupExportTool(BaseTool):
    """Backs up and exports important NEXUS data."""

    name = "backup_export"
    description = "NEXUSの知識データをバックアップ・エクスポートします"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return text in {
            "NEXUSバックアップ",
            "知識バックアップ",
            "知識エクスポート",
            "バックアップ一覧",
        }

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "NEXUSバックアップ":
            return self._nexus_backup()

        if text == "知識バックアップ":
            return self._knowledge_backup()

        if text == "知識エクスポート":
            return self._knowledge_export()

        if text == "バックアップ一覧":
            return self._backup_list()

        return "対応していないバックアップ操作です。"

    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _nexus_backup(self) -> str:
        stamp = self._timestamp()
        backup_root = Path("backups") / "nexus_manual" / stamp
        backup_root.mkdir(parents=True, exist_ok=True)

        targets = [
            "data/knowledge",
            "prompts",
            "docs",
            "config",
        ]

        copied = []

        for target in targets:
            src = Path(target)

            if not src.exists():
                continue

            dst = backup_root / target
            dst.parent.mkdir(parents=True, exist_ok=True)

            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

            copied.append(target)

        zip_path = Path("backups") / "nexus_manual" / f"nexus_backup_{stamp}.zip"
        self._zip_dir(backup_root, zip_path)

        return (
            "## NEXUS Backup Completed\n\n"
            f"- Backup Directory: {backup_root}\n"
            f"- Zip: {zip_path}\n"
            f"- Copied: {len(copied)} targets\n\n"
            + "\n".join(f"- {item}" for item in copied)
        )

    def _knowledge_backup(self) -> str:
        stamp = self._timestamp()
        backup_root = Path("backups") / "knowledge_manual" / stamp
        backup_root.mkdir(parents=True, exist_ok=True)

        src = Path("data/knowledge")

        if not src.exists():
            return "## Knowledge Backup\n\n`data/knowledge` が見つかりません。"

        dst = backup_root / "data" / "knowledge"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)

        zip_path = Path("backups") / "knowledge_manual" / f"knowledge_backup_{stamp}.zip"
        self._zip_dir(backup_root, zip_path)

        return (
            "## Knowledge Backup Completed\n\n"
            f"- Backup Directory: {backup_root}\n"
            f"- Zip: {zip_path}\n"
            "- Target: data/knowledge\n\n"
            "削除や変更はしていません。"
        )

    def _knowledge_export(self) -> str:
        stamp = self._timestamp()
        export_dir = Path("exports") / f"knowledge_export_{stamp}"
        export_dir.mkdir(parents=True, exist_ok=True)

        knowledge_path = Path("data/knowledge/knowledge.json")
        world_updates_path = Path("data/knowledge/world_updates.json")
        source_registry_path = Path("data/knowledge/source_registry.json")
        search_settings_path = Path("data/knowledge/search_settings.json")
        auto_recall_path = Path("data/knowledge/auto_recall_settings.json")

        files = [
            knowledge_path,
            world_updates_path,
            source_registry_path,
            search_settings_path,
            auto_recall_path,
        ]

        copied = []

        for src in files:
            if src.exists():
                dst = export_dir / src.name
                shutil.copy2(src, dst)
                copied.append(src.name)

        summary_path = export_dir / "SUMMARY.md"
        summary_path.write_text(self._export_summary(), encoding="utf-8")

        zip_path = Path("exports") / f"knowledge_export_{stamp}.zip"
        self._zip_dir(export_dir, zip_path)

        return (
            "## Knowledge Export Completed\n\n"
            f"- Export Directory: {export_dir}\n"
            f"- Zip: {zip_path}\n"
            f"- Files: {len(copied)}\n\n"
            + "\n".join(f"- {item}" for item in copied)
            + "\n- SUMMARY.md"
        )

    def _backup_list(self) -> str:
        roots = [
            Path("backups/nexus_manual"),
            Path("backups/knowledge_manual"),
            Path("backups/backup_export_v1"),
            Path("exports"),
        ]

        lines = [
            "## Backup / Export List",
            "",
        ]

        found = False

        for root in roots:
            lines.append(f"### {root}")

            if not root.exists():
                lines.append("- なし")
                lines.append("")
                continue

            items = sorted(root.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)[:12]

            if not items:
                lines.append("- なし")
                lines.append("")
                continue

            found = True

            for item in items:
                kind = "dir" if item.is_dir() else "file"
                size = self._safe_size(item)
                lines.append(f"- [{kind}] {item} ({size})")

            lines.append("")

        if not found:
            lines.append("バックアップやエクスポートはまだ見つかりません。")

        return "\n".join(lines).rstrip()

    def _export_summary(self) -> str:
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        world_updates = self._load_json("data/knowledge/world_updates.json", [])
        sources = self._load_json("data/knowledge/source_registry.json", [])

        if not isinstance(knowledge, list):
            knowledge = []

        by_category = {}
        archived = 0

        for entry in knowledge:
            category = entry.get("category", "unknown")
            by_category[category] = by_category.get(category, 0) + 1

            if entry.get("archived"):
                archived += 1

        lines = [
            "# NEXUS Knowledge Export Summary",
            "",
            f"Exported At: {datetime.now().isoformat(timespec='seconds')}",
            "",
            "## Counts",
            "",
            f"- Knowledge Entries: {len(knowledge)}",
            f"- Archived Entries: {archived}",
            f"- World Update Logs: {len(world_updates) if isinstance(world_updates, list) else 0}",
            f"- Source Registry Entries: {len(sources) if isinstance(sources, list) else 0}",
            "",
            "## Categories",
            "",
        ]

        for category, count in sorted(by_category.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {category}: {count}")

        lines.append("")
        lines.append("## Notes")
        lines.append("")
        lines.append("- This export is a local safety copy.")
        lines.append("- It does not delete or rewrite original data.")
        lines.append("- Check source and license before using paper or news content.")

        return "\n".join(lines) + "\n"

    def _load_json(self, path_text: str, default):
        path = Path(path_text)

        if not path.exists():
            return default

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _zip_dir(self, src_dir: Path, zip_path: Path) -> None:
        zip_path.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in src_dir.rglob("*"):
                if path.is_file():
                    archive.write(path, path.relative_to(src_dir))

    def _safe_size(self, path: Path) -> str:
        try:
            if path.is_dir():
                total = sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
            else:
                total = path.stat().st_size
        except Exception:
            return "unknown"

        if total >= 1024 * 1024:
            return f"{total / (1024 * 1024):.1f} MB"

        if total >= 1024:
            return f"{total / 1024:.1f} KB"

        return f"{total} B"
