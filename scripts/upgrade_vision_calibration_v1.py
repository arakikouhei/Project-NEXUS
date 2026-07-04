from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "vision_calibration_v1" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def patch_vision_tool() -> None:
    path = ROOT / "nexus/tools/vision.py"
    text = path.read_text(encoding="utf-8")

    # can_handle に画像意味テストを追加
    if 'or text == "画像意味テスト"' not in text:
        text = text.replace(
            '            or text == "画像ヘルプ"\n',
            '            or text == "画像ヘルプ"\n'
            '            or text == "画像意味テスト"\n',
            1,
        )

    # execute に画像意味テストを追加
    if 'if text == "画像意味テスト":' not in text:
        text = text.replace(
            '        if text in {"画像ヘルプ", "vision help"}:\n'
            '            return self._help()\n',
            '        if text in {"画像ヘルプ", "vision help"}:\n'
            '            return self._help()\n\n'
            '        if text == "画像意味テスト":\n'
            '            return self._semantic_test()\n',
            1,
        )

    path.write_text(text, encoding="utf-8")

    replace_method(
        "nexus/tools/vision.py",
        "_semantic_scores",
        '''    def _semantic_scores(
        self,
        mean_rgb: list[float],
        brightness: float,
        contrast: float,
        saturation: float,
        edge_score: float,
        color_variety: float,
        width: int,
        height: int,
    ) -> list[tuple[str, int]]:
        """
        Vision Calibration v1

        This is still heuristic scoring, not object recognition.
        Main fix:
        - Low saturation alone should not make mineral score too high.
        - Green dominance should raise plant score more clearly.
        - Illustration/photo should be separated by color variety and edge behavior.
        """
        r, g, b = mean_rgb
        aspect = width / height if height else 1.0

        max_rgb = max(r, g, b)
        min_rgb = min(r, g, b)
        rgb_range = max_rgb - min_rgb

        green_dominance = max(0.0, g - max(r, b))
        green_ratio = g / max(1.0, (r + b) / 2.0)
        gray_balance = 100.0 - min(100.0, rgb_range)
        hard_surface_signal = (contrast * 0.65) + (edge_score * 0.35)

        # 植物っぽさ:
        # 緑優勢 + ある程度の彩度 + 明るすぎ/暗すぎない条件で上げる
        plant = 12
        plant += min(50, green_dominance * 1.15)
        plant += 18 if green_ratio > 1.08 else 0
        plant += 12 if saturation > 18 else 0
        plant += 10 if 45 < brightness < 220 else 0
        plant -= 12 if saturation < 10 else 0

        # 石・鉱物っぽさ:
        # 低彩度だけでは上げすぎない。
        # 灰色寄り + 中〜高コントラスト + 緑優勢が弱い場合に上げる
        mineral = 15
        mineral += 18 if saturation < 22 else 0
        mineral += 18 if gray_balance > 70 else 0
        mineral += 18 if contrast > 35 else 0
        mineral += 8 if edge_score > 10 else 0
        mineral -= 28 if green_ratio > 1.08 and saturation > 15 else 0
        mineral -= 10 if color_variety < 12 and green_ratio > 1.03 else 0

        # 人工物っぽさ:
        # 輪郭・コントラスト・鮮やかさ・低自然色で上げる
        artificial = 18
        artificial += min(25, hard_surface_signal * 0.32)
        artificial += 14 if contrast > 45 else 0
        artificial += 12 if edge_score > 16 else 0
        artificial += 12 if saturation > 42 else 0
        artificial -= 8 if green_ratio > 1.12 and saturation > 18 else 0

        # イラストっぽさ:
        # 色数少なめ + 輪郭 + 平坦色で上げる
        illustration = 14
        illustration += 24 if color_variety < 25 else 0
        illustration += 18 if edge_score > 14 and contrast > 30 else 0
        illustration += 12 if saturation > 18 and color_variety < 35 else 0
        illustration += 8 if rgb_range > 20 and color_variety < 20 else 0

        # 写真っぽさ:
        # 色数と微妙な変化が多いほど上げる。
        # サンプルのような単純図形では上がりすぎないよう調整。
        photo = 20
        photo += 26 if color_variety > 45 else 0
        photo += 12 if 20 < contrast < 80 else 0
        photo += 10 if 8 < saturation < 75 else 0
        photo += 8 if 8 < edge_score < 35 else 0
        photo -= 16 if color_variety < 18 else 0

        # 背景っぽさ:
        # 横長・低コントラスト・低彩度・色数少なめで上げる
        background = 22
        background += 16 if aspect > 1.2 else 0
        background += 14 if contrast < 38 else 0
        background += 12 if saturation < 35 else 0
        background += 10 if color_variety < 30 else 0

        scores = [
            ("植物っぽさ", plant),
            ("石・鉱物っぽさ", mineral),
            ("人工物っぽさ", artificial),
            ("イラストっぽさ", illustration),
            ("写真っぽさ", photo),
            ("背景っぽさ", background),
        ]

        return [(label, self._clamp_score(score)) for label, score in scores]''',
    )

    # _help の前に _semantic_test を追加
    text = path.read_text(encoding="utf-8")
    if "def _semantic_test(self)" not in text:
        marker = "    def _help(self) -> str:\n"
        method = '''    def _semantic_test(self) -> str:
        samples = [
            ("green_sample", "tests/assets/vision_green_sample.png"),
            ("gray_sample", "tests/assets/vision_gray_sample.png"),
            ("graphic_sample", "tests/assets/vision_graphic_sample.png"),
            ("original_sample", "tests/assets/sample_vision.png"),
        ]

        lines = [
            "## Vision Semantic Test",
            "",
        ]

        for label, path_text in samples:
            result = self._semantic_analyze(path_text)
            lines.append(f"### {label}")
            if "### Semantic Scores" in result:
                section = result.split("### Semantic Scores", 1)[1]
                section = section.split("### Reading", 1)[0].strip()
                lines.append(section)
            else:
                lines.append(result[:500])
            lines.append("")

        lines.append("Notes:")
        lines.append("- これは回帰確認用の簡易テストです。")
        lines.append("- スコアは推定であり、対象名の確定ではありません。")

        return "\\n".join(lines)

'''
        if marker not in text:
            raise SystemExit("vision.py: _help が見つかりません。")
        text = text.replace(marker, method + marker, 1)

    # help文に画像意味テストを追加
    if "- 画像意味テスト\\n" not in text:
        text = text.replace(
            '- 画像意味分析: /path/to/image.png\\n\\n',
            '- 画像意味分析: /path/to/image.png\\n'
            '- 画像意味テスト\\n\\n',
            1,
        )

    path.write_text(text, encoding="utf-8")


def create_test_images() -> None:
    from PIL import Image, ImageDraw

    assets = ROOT / "tests" / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    # 緑・植物寄りサンプル
    img = Image.new("RGB", (640, 360), (205, 230, 205))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 250, 640, 360), fill=(80, 135, 80))
    draw.ellipse((100, 60, 270, 240), fill=(45, 150, 65))
    draw.ellipse((240, 45, 450, 250), fill=(55, 165, 80))
    draw.ellipse((390, 90, 570, 260), fill=(40, 130, 70))
    img.save(assets / "vision_green_sample.png")

    # 灰色・鉱物寄りサンプル
    img = Image.new("RGB", (640, 360), (160, 160, 160))
    draw = ImageDraw.Draw(img)
    draw.polygon([(80, 280), (210, 90), (360, 260)], fill=(115, 115, 120))
    draw.polygon([(280, 300), (420, 70), (570, 270)], fill=(95, 98, 105))
    draw.line((80, 280, 210, 90, 360, 260), fill=(210, 210, 215), width=4)
    draw.line((280, 300, 420, 70, 570, 270), fill=(205, 205, 210), width=4)
    img.save(assets / "vision_gray_sample.png")

    # 図形・人工物/イラスト寄りサンプル
    img = Image.new("RGB", (640, 360), (245, 245, 245))
    draw = ImageDraw.Draw(img)
    draw.rectangle((80, 80, 260, 260), fill=(220, 60, 60))
    draw.ellipse((320, 70, 520, 270), fill=(60, 120, 230))
    draw.line((50, 310, 590, 310), fill=(40, 40, 40), width=8)
    img.save(assets / "vision_graphic_sample.png")


def patch_diagnostics() -> None:
    path = ROOT / "nexus/tools/diagnostics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    if '"画像意味テスト"' not in text:
        text = text.replace(
            '                    "画像意味分析: tests/assets/sample_vision.png",\n',
            '                    "画像意味分析: tests/assets/sample_vision.png",\n'
            '                    "画像意味テスト",\n',
            1,
        )

    path.write_text(text, encoding="utf-8")


def write_docs() -> None:
    path = ROOT / "docs/VISION_CALIBRATION_V1.md"
    path.write_text(
        """# Vision Calibration v1

Adjusted semantic scoring.

## Changes

- Green-dominant images score higher for plant-like tendency.
- Low saturation alone no longer over-boosts mineral-like tendency.
- Photo-like score is reduced for very simple low-variety graphic images.
- Added semantic test samples.

## Command

- 画像意味テスト

## Limits

Still heuristic. This is not object recognition.
""",
        encoding="utf-8",
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/tools/vision.py",
        "nexus/tools/diagnostics.py",
    ]:
        backup(target)

    patch_vision_tool()
    create_test_images()
    patch_diagnostics()
    write_docs()

    print("Vision Calibration v1 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
