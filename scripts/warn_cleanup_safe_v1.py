from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "warn_cleanup_safe_v1" / datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return
    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def replace_method(path_text: str, method_name: str, new_method: str) -> None:
    path = ROOT / path_text
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"    def {method_name}("):
            start = i
            break

    if start is None:
        raise SystemExit(f"{path_text}: {method_name} が見つかりません。")

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("    def "):
            end = j
            break

    new_lines = lines[:start] + new_method.rstrip().splitlines() + lines[end:]
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def patch_capability() -> None:
    replace_method(
        "nexus/tools/capability.py",
        "can_handle",
        '''    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        # 画像系ヘルプはVisionTool専用
        if text.startswith(("画像", "vision")):
            return False

        keywords = [
            "できること",
            "機能一覧",
            "ヘルプ",
            "使い方",
            "何ができる",
        ]

        return text in keywords''',
    )


def patch_project() -> None:
    replace_method(
        "nexus/tools/project.py",
        "can_handle",
        '''    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        # 検索/調査系はSafeSearchTool/SafeResearchTool専用
        if text.startswith((
            "安全検索:",
            "安全検索：",
            "公式確認:",
            "公式確認：",
            "公式検索:",
            "公式検索：",
            "調べて:",
            "調べて：",
            "用語確認:",
            "用語確認：",
            "wiki検索:",
            "wiki検索：",
        )):
            return False

        keywords = [
            "どこ",
            "探して",
            "場所",
            "ファイル",
            "コード",
        ]

        return any(word in text for word in keywords)''',
    )


def patch_filesystem() -> None:
    replace_method(
        "nexus/tools/filesystem.py",
        "can_handle",
        '''    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        # アプリ系はAppControlTool専用
        if text.startswith((
            "アプリ",
            "Chrome",
            "Google Chrome",
            "VS Code",
            "Visual Studio Code",
            "Finder",
            "Maya",
            "Premiere",
            "Premiere Pro",
        )):
            return False

        keywords = [
            "フォルダ一覧",
            "README",
            "main.py",
            "console.py",
        ]

        return any(word in text for word in keywords)''',
    )


def patch_math() -> None:
    replace_method(
        "nexus/tools/math.py",
        "can_handle",
        '''    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        # 基本計算はCalculatorTool専用
        if text.startswith(("計算:", "計算：", "calc:", "calc：")):
            return False

        advanced_prefixes = (
            "単位変換:",
            "単位変換：",
            "方程式:",
            "方程式：",
            "因数分解:",
            "因数分解：",
            "展開:",
            "展開：",
            "微分:",
            "微分：",
            "積分:",
            "積分：",
            "平方完成:",
            "平方完成：",
        )

        if text.startswith(advanced_prefixes):
            return True

        return text in {"数学ヘルプ", "math help"}''',
    )


def write_docs() -> None:
    path = ROOT / "docs/WARN_CLEANUP_SAFE_V1.md"
    path.write_text(
        """# WARN Cleanup Safe v1

Reduced tool collision warnings by replacing only can_handle methods.

## Fixed

- 画像ヘルプ no longer collides with CapabilityTool.
- 安全検索 no longer collides with ProjectTool.
- アプリ一覧 no longer collides with FileSystemTool.
- 計算: no longer collides with AdvancedMathTool.

""",
        encoding="utf-8",
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/tools/capability.py",
        "nexus/tools/project.py",
        "nexus/tools/filesystem.py",
        "nexus/tools/math.py",
    ]:
        backup(target)

    patch_capability()
    patch_project()
    patch_filesystem()
    patch_math()
    write_docs()

    print("WARN Cleanup Safe v1 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
