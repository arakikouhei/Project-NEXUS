from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import re


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "vision_semantic_v2" / datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return
    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def patch_vision_tool() -> None:
    path = ROOT / "nexus/tools/vision.py"
    text = path.read_text(encoding="utf-8")

    if "Vision Semantic Layer v2" in text:
        print("vision.py already has semantic v2")
        return

    # 1. can_handle に画像意味分析を追加
    text = text.replace(
        '                    or text.startswith("画像分析:")\n'
        '                    or text.startswith("画像分析：")\n',
        '                    or text.startswith("画像分析:")\n'
        '                    or text.startswith("画像分析：")\n'
        '                    or text.startswith("画像意味分析:")\n'
        '                    or text.startswith("画像意味分析：")\n',
        1,
    )

    # 2. execute に分岐を追加
    text = text.replace(
        '                if text.startswith(("画像分析:", "画像分析：")):\n'
        '                    path = self._extract_path(text)\n'
        '                    return self._analyze(path)\n\n'
        '                return "対応していない画像操作です。"\n',
        '                if text.startswith(("画像分析:", "画像分析：")):\n'
        '                    path = self._extract_path(text)\n'
        '                    return self._analyze(path)\n\n'
        '                if text.startswith(("画像意味分析:", "画像意味分析：")):\n'
        '                    path = self._extract_path(text)\n'
        '                    return self._semantic_analyze(path)\n\n'
        '                return "対応していない画像操作です。"\n',
        1,
    )

    # 3. helpに追加
    text = text.replace(
        "- 画像分析: /path/to/image.png\\n\\n"
        "例:\\n"
        "- 画像分析: tests/assets/sample_vision.png\\n\\n",
        "- 画像分析: /path/to/image.png\\n"
        "- 画像意味分析: /path/to/image.png\\n\\n"
        "例:\\n"
        "- 画像分析: tests/assets/sample_vision.png\\n"
        "- 画像意味分析: tests/assets/sample_vision.png\\n\\n",
        1,
    )

    # 4. _help のまだできないことの前に説明を足す
    text = text.replace(
        "- 植物/鉱物/人工物っぽさの簡易ヒント\\n\\n"
        "まだできないこと:\\n",
        "- 植物/鉱物/人工物っぽさの簡易ヒント\\n"
        "- 意味分析 v2: 植物/鉱物/人工物/イラスト/写真/背景っぽさのスコア\\n\\n"
        "まだできないこと:\\n",
        1,
    )

    # 5. クラス末尾の _help の前に semantic methods を入れる
    marker = "            def _help(self) -> str:\n"

    semantic_methods = r'''
            # Vision Semantic Layer v2
            def _semantic_analyze(self, path_text: str) -> str:
                ok, message, path = self._basic_file_check(path_text)

                if not ok:
                    return f"## Vision Semantic Analysis\n\n分析できません。\nReason: {message}"

                try:
                    from PIL import Image, ImageStat

                    assert path is not None

                    with Image.open(path) as image:
                        original_format = image.format or "unknown"
                        width, height = image.size
                        mode = image.mode

                        rgb = image.convert("RGB")
                        small = rgb.copy()
                        small.thumbnail((256, 256))

                        stat = ImageStat.Stat(small)
                        mean_rgb = stat.mean
                        std_rgb = stat.stddev

                        brightness = sum(mean_rgb) / 3
                        contrast = sum(std_rgb) / 3
                        saturation = self._average_saturation(small)
                        dominant = self._dominant_colors(small)
                        edge_score = self._edge_score(small)
                        color_variety = self._color_variety(small)

                    orientation = self._orientation(width, height)

                    scores = self._semantic_scores(
                        mean_rgb=mean_rgb,
                        brightness=brightness,
                        contrast=contrast,
                        saturation=saturation,
                        edge_score=edge_score,
                        color_variety=color_variety,
                        width=width,
                        height=height,
                    )

                    interpretation = self._semantic_interpretation(scores)

                    score_lines = []
                    for label, score in scores:
                        bar = self._score_bar(score)
                        score_lines.append(f"- {label}: {score:3d}/100 {bar}")

                    return (
                        "## Vision Semantic Analysis\n\n"
                        f"File: {path}\n"
                        f"Format: {original_format}\n"
                        f"Mode: {mode}\n"
                        f"Size: {width} x {height}px\n"
                        f"Orientation: {orientation}\n\n"
                        "### Semantic Scores\n"
                        + "\n".join(score_lines)
                        + "\n\n"
                        "### Reading\n"
                        + "\n".join(f"- {line}" for line in interpretation)
                        + "\n\n"
                        "### Basic Signals\n"
                        f"- Brightness: {brightness:.1f} / 255\n"
                        f"- Contrast: {contrast:.1f}\n"
                        f"- Saturation: {saturation:.1f} / 100\n"
                        f"- Edge Score: {edge_score:.1f}\n"
                        f"- Color Variety: {color_variety:.1f}\n"
                        + "\n\n"
                        "### Dominant Colors\n"
                        + "\n".join(f"- RGB{color}" for color in dominant)
                        + "\n\n"
                        "### Limits\n"
                        "- これはローカル特徴量による意味推定です。\n"
                        "- 物体名・植物名・鉱物名は断定しません。\n"
                        "- 人物の個人特定はしません。\n"
                        "- 本格的な画像認識AIではなく、Vision Modelへ進む前の意味分析層です。"
                    )

                except Exception as error:
                    return f"画像意味分析に失敗しました: {error}"

            def _edge_score(self, image) -> float:
                try:
                    from PIL import ImageFilter, ImageStat

                    gray = image.resize((128, 128)).convert("L")
                    edges = gray.filter(ImageFilter.FIND_EDGES)
                    stat = ImageStat.Stat(edges)
                    return float(stat.mean[0])
                except Exception:
                    return 0.0

            def _color_variety(self, image) -> float:
                try:
                    small = image.resize((64, 64)).convert("RGB")
                    colors = small.getcolors(maxcolors=4096)

                    if not colors:
                        return 100.0

                    unique = len(colors)
                    return min(100.0, unique / 40.0)
                except Exception:
                    return 0.0

            def _semantic_scores(
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
                r, g, b = mean_rgb
                aspect = width / height if height else 1.0

                green_strength = max(0.0, g - max(r, b))
                gray_balance = 100.0 - min(100.0, (abs(r - g) + abs(g - b) + abs(b - r)) / 3.0)
                vividness = saturation
                hard_surface_signal = (contrast * 0.55) + (edge_score * 0.45)

                plant = 20
                plant += min(45, green_strength * 0.8)
                plant += 15 if saturation > 25 else 0
                plant += 10 if brightness > 55 and brightness < 210 else 0
                plant -= 10 if gray_balance > 80 and saturation < 20 else 0

                mineral = 20
                mineral += 30 if saturation < 25 else 0
                mineral += min(25, gray_balance * 0.25)
                mineral += 15 if contrast > 30 else 0
                mineral -= 10 if green_strength > 30 and saturation > 25 else 0

                artificial = 20
                artificial += min(30, hard_surface_signal * 0.4)
                artificial += 15 if contrast > 45 else 0
                artificial += 15 if saturation > 45 else 0
                artificial += 10 if edge_score > 18 else 0

                illustration = 15
                illustration += 25 if color_variety < 35 else 0
                illustration += 20 if edge_score > 18 and saturation > 25 else 0
                illustration += 15 if contrast > 40 else 0
                illustration += 10 if vividness > 45 else 0

                photo = 25
                photo += 25 if color_variety > 35 else 0
                photo += 15 if contrast > 20 and contrast < 75 else 0
                photo += 15 if saturation > 10 and saturation < 70 else 0
                photo += 10 if edge_score < 35 else 0

                background = 25
                background += 20 if contrast < 35 else 0
                background += 15 if saturation < 35 else 0
                background += 10 if aspect > 1.2 else 0
                background += 10 if color_variety < 45 else 0

                scores = [
                    ("植物っぽさ", plant),
                    ("石・鉱物っぽさ", mineral),
                    ("人工物っぽさ", artificial),
                    ("イラストっぽさ", illustration),
                    ("写真っぽさ", photo),
                    ("背景っぽさ", background),
                ]

                return [(label, self._clamp_score(score)) for label, score in scores]

            def _semantic_interpretation(self, scores: list[tuple[str, int]]) -> list[str]:
                ordered = sorted(scores, key=lambda item: item[1], reverse=True)
                top_label, top_score = ordered[0]
                second_label, second_score = ordered[1]

                lines = []

                if top_score >= 70:
                    lines.append(f"最も強い傾向は「{top_label}」です。")
                elif top_score >= 50:
                    lines.append(f"やや強い傾向として「{top_label}」があります。")
                else:
                    lines.append("決定的な傾向は弱く、複数の可能性が混ざっています。")

                if second_score >= 50:
                    lines.append(f"次に「{second_label}」の傾向もあります。")

                if "植物" in top_label:
                    lines.append("緑成分や彩度が影響して、自然物・植物寄りに見えています。")
                elif "鉱物" in top_label:
                    lines.append("低彩度や灰色寄りの成分が影響して、石・鉱物・硬い素材寄りに見えています。")
                elif "人工物" in top_label:
                    lines.append("輪郭・コントラスト・彩度の出方から、人工物寄りに見えています。")
                elif "イラスト" in top_label:
                    lines.append("色数や輪郭の出方から、イラスト・図像寄りの可能性があります。")
                elif "写真" in top_label:
                    lines.append("色や明暗のばらつきから、写真寄りの可能性があります。")
                elif "背景" in top_label:
                    lines.append("全体の均一さから、背景・面・風景の一部寄りに見えています。")

                lines.append("ただし、これは画像特徴からの推定であり、対象名の確定ではありません。")

                return lines

            def _score_bar(self, score: int) -> str:
                filled = max(0, min(10, round(score / 10)))
                return "[" + "█" * filled + "░" * (10 - filled) + "]"

            def _clamp_score(self, value: float) -> int:
                return int(max(0, min(100, round(value))))

'''

    if marker not in text:
        raise SystemExit("vision.py の _help メソッドが見つかりません。")

    text = text.replace(marker, semantic_methods + marker, 1)

    path.write_text(text, encoding="utf-8")


def patch_agent_bypass() -> None:
    path = ROOT / "nexus/agent/agent.py"
    text = path.read_text(encoding="utf-8")

    if '"画像意味分析:"' in text:
        return

    text = text.replace(
        '            "画像分析:",\n'
        '            "画像分析：",\n',
        '            "画像分析:",\n'
        '            "画像分析：",\n'
        '            "画像意味分析:",\n'
        '            "画像意味分析：",\n',
        1,
    )

    path.write_text(text, encoding="utf-8")


def patch_diagnostics() -> None:
    path = ROOT / "nexus/tools/diagnostics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    if '"画像意味分析: tests/assets/sample_vision.png"' in text:
        return

    text = text.replace(
        '                    "画像分析: tests/assets/sample_vision.png",\n',
        '                    "画像分析: tests/assets/sample_vision.png",\n'
        '                    "画像意味分析: tests/assets/sample_vision.png",\n',
        1,
    )

    path.write_text(text, encoding="utf-8")


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    if not path.exists():
        path.write_text("あなたは Project NEXUS です。\n", encoding="utf-8")

    text = path.read_text(encoding="utf-8")
    marker = "# Vision Semantic Layer v2"

    if marker in text:
        return

    addition = """

# Vision Semantic Layer v2

NEXUSは画像の基礎分析に加えて、意味寄りの推定ができます。

使える例:
- 画像意味分析: /path/to/image.png
- 画像意味分析: tests/assets/sample_vision.png

推定できる傾向:
- 植物っぽさ
- 石・鉱物っぽさ
- 人工物っぽさ
- イラストっぽさ
- 写真っぽさ
- 背景っぽさ

注意:
- 物体名・植物名・鉱物名は断定しません。
- 人物の個人特定はしません。
- これはローカル特徴量による推定であり、本格画像認識AIではありません。
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    path = ROOT / "docs/VISION_SEMANTIC_LAYER_V2.md"
    path.write_text(
        """# Vision Semantic Layer v2

Adds semantic-like local image analysis.

## Command

- 画像意味分析: /path/to/image.png

## Scores

- 植物っぽさ
- 石・鉱物っぽさ
- 人工物っぽさ
- イラストっぽさ
- 写真っぽさ
- 背景っぽさ

## Limits

This is not full object recognition.
It does not identify exact plant names, mineral names, people, or dangerous objects.
""",
        encoding="utf-8",
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/tools/vision.py",
        "nexus/agent/agent.py",
        "nexus/tools/diagnostics.py",
        "prompts/system_prompt.txt",
    ]:
        backup(target)

    patch_vision_tool()
    patch_agent_bypass()
    patch_diagnostics()
    patch_system_prompt()
    write_docs()

    print("Vision Semantic Layer v2 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
