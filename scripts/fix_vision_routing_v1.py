from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import re


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "vision_routing_fix_v1" / datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return
    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def patch_tool_manager() -> None:
    path = ROOT / "nexus/tools/manager.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.tools.vision import VisionTool" not in text:
        # safe_search があればその後ろに追加
        if "from nexus.tools.safe_search import SafeSearchTool\n" in text:
            text = text.replace(
                "from nexus.tools.safe_search import SafeSearchTool\n",
                "from nexus.tools.safe_search import SafeSearchTool\n"
                "from nexus.tools.vision import VisionTool\n",
                1,
            )
        elif "from nexus.tools.web import WebTool\n" in text:
            text = text.replace(
                "from nexus.tools.web import WebTool\n",
                "from nexus.tools.web import WebTool\n"
                "from nexus.tools.vision import VisionTool\n",
                1,
            )
        else:
            text += "\nfrom nexus.tools.vision import VisionTool\n"

    # VisionTool登録の重複を一度消す
    text = re.sub(r"\n\s*self\.register\(VisionTool\(\)\)", "", text)

    # Calculator / AdvancedMath より前に必ず入れる
    insert_line = "                self.register(VisionTool())\n"

    candidates = [
        "                self.register(SafeSearchTool())\n",
        "                self.register(SafeResearchTool())\n",
        "                self.register(WebTool())\n",
        "                self.register(AppControlTool())\n",
        "                self.register(AdvancedMathTool())\n",
        "                self.register(CalculatorTool())\n",
    ]

    inserted = False

    for candidate in candidates:
        if candidate in text:
            text = text.replace(candidate, candidate + insert_line, 1)
            inserted = True
            break

    if not inserted:
        raise SystemExit("ToolManager内の登録位置を見つけられませんでした。")

    path.write_text(text, encoding="utf-8")


def patch_agent_bypass_normalizer() -> None:
    path = ROOT / "nexus/agent/agent.py"
    text = path.read_text(encoding="utf-8")

    marker = "# VISION_ROUTING_BYPASS"

    if marker in text:
        path.write_text(text, encoding="utf-8")
        return

    pattern = r"(    def process\(self, user_input: str\) -> tuple\[bool, str \| None\]:\n)"

    insert = '''\\1        # VISION_ROUTING_BYPASS
        # 画像系コマンドは InputNormalizer を通すと「ヘルプ」や計算に誤分類されるため、
        # 先にVisionToolへ渡す。
        stripped_input = user_input.strip()
        vision_prefixes = (
            "画像ヘルプ",
            "vision help",
            "画像安全確認:",
            "画像安全確認：",
            "画像分析:",
            "画像分析：",
        )

        if stripped_input.startswith(vision_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

'''

    new_text, count = re.subn(pattern, insert, text, count=1)

    if count != 1:
        raise SystemExit("agent.py の process 関数を見つけられませんでした。")

    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    backup("nexus/tools/manager.py")
    backup("nexus/agent/agent.py")

    patch_tool_manager()
    patch_agent_bypass_normalizer()

    print("Vision routing fix applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
