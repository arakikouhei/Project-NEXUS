"""
Project NEXUS
Knowledge Import Tool v1

Imports local .txt / .md notes into Knowledge Core safely.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import json

from nexus.tools.base_tool import BaseTool


class KnowledgeImportTool(BaseTool):
    """Imports local text or markdown files into knowledge.json."""

    name = "knowledge_import"
    description = "ローカルのtxt/mdメモをNEXUS知識として安全に取り込みます"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text.startswith("知識インポート:")
            or text.startswith("メモ取り込み:")
            or text.startswith("インポート確認:")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text.startswith("インポート確認:"):
            path_text = text.split(":", 1)[1].strip()
            return self._preview_import(path_text)

        if text.startswith("知識インポート:"):
            path_text = text.split(":", 1)[1].strip()
            return self._import_file(path_text)

        if text.startswith("メモ取り込み:"):
            path_text = text.split(":", 1)[1].strip()
            return self._import_file(path_text)

        return "対応していないインポート操作です。"

    def _resolve_path(self, path_text: str) -> Path:
        path_text = path_text.strip().strip('"').strip("'")
        return Path(path_text).expanduser()

    def _validate_file(self, path: Path) -> tuple[bool, str]:
        if not path.exists():
            return False, f"ファイルが見つかりません: {path}"

        if not path.is_file():
            return False, f"ファイルではありません: {path}"

        if path.suffix.lower() not in {".txt", ".md", ".markdown"}:
            return False, "取り込める形式は .txt / .md / .markdown です。"

        try:
            size = path.stat().st_size
        except Exception:
            return False, "ファイルサイズを確認できません。"

        if size == 0:
            return False, "空ファイルは取り込めません。"

        if size > 300_000:
            return False, "ファイルが大きすぎます。v1では300KB以下にしてください。"

        return True, "OK"

    def _read_text(self, path: Path) -> str:
        for encoding in ("utf-8", "utf-8-sig", "cp932"):
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue

        return path.read_text(encoding="utf-8", errors="replace")

    def _preview_import(self, path_text: str) -> str:
        path = self._resolve_path(path_text)
        ok, message = self._validate_file(path)

        if not ok:
            return f"## Import Preview Failed\n\n- Reason: {message}"

        content = self._read_text(path)
        title = self._guess_title(path, content)
        digest = self._digest(content)
        preview = content.strip().replace("\r\n", "\n")[:1200]

        return f"""## Import Preview

- File: {path}
- Title: {title}
- Size: {path.stat().st_size} bytes
- Digest: {digest}
- Category: imported
- Source Type: local_file

### Preview

{preview}
"""

    def _import_file(self, path_text: str) -> str:
        path = self._resolve_path(path_text)
        ok, message = self._validate_file(path)

        if not ok:
            return f"## Knowledge Import Failed\n\n- Reason: {message}"

        knowledge_path = Path("data/knowledge/knowledge.json")
        knowledge_path.parent.mkdir(parents=True, exist_ok=True)

        knowledge = self._load_knowledge(knowledge_path)

        content = self._read_text(path).strip()
        digest = self._digest(content)

        duplicate = self._find_duplicate(knowledge, digest, str(path))

        if duplicate:
            return f"""## Knowledge Import Skipped

同じ内容または同じsource_pathの知識が既にあります。

- Existing ID: {duplicate.get('id', 'unknown')}
- Title: {duplicate.get('title', 'unknown')}
- Source Path: {duplicate.get('source_path', 'unknown')}
"""

        entry_id = f"imported-{digest[:8]}"
        title = self._guess_title(path, content)

        entry = {
            "id": entry_id,
            "category": "imported",
            "title": title,
            "content": content,
            "tags": self._guess_tags(path, content),
            "source": "local_file",
            "source_type": "local_file",
            "source_path": str(path),
            "digest": digest,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "archived": False,
        }

        knowledge.append(entry)
        knowledge_path.write_text(
            json.dumps(knowledge, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return f"""## Knowledge Import Completed

- ID: {entry_id}
- Title: {title}
- Category: imported
- Source Path: {path}
- Tags: {", ".join(entry["tags"])}
- Characters: {len(content)}

確認:
- 知識詳細: {entry_id}
- 知識検索: {title}
"""

    def _load_knowledge(self, path: Path) -> list:
        if not path.exists():
            return []

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _find_duplicate(self, knowledge: list, digest: str, source_path: str) -> dict | None:
        for entry in knowledge:
            if not isinstance(entry, dict):
                continue

            if entry.get("digest") == digest:
                return entry

            if entry.get("source_path") == source_path:
                return entry

        return None

    def _digest(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _guess_title(self, path: Path, content: str) -> str:
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        if lines:
            first = lines[0].lstrip("#").strip()
            if first:
                return first[:80]

        return path.stem[:80]

    def _guess_tags(self, path: Path, content: str) -> list[str]:
        tags = ["imported", "local_note"]

        suffix = path.suffix.lower().replace(".", "")
        if suffix:
            tags.append(suffix)

        lowered = content.lower()

        if "maya" in lowered or "uv" in lowered:
            tags.append("3dcg")

        if "paper" in lowered or "arxiv" in lowered or "論文" in content:
            tags.append("papers")

        if "nexus" in lowered:
            tags.append("nexus")

        return list(dict.fromkeys(tags))
