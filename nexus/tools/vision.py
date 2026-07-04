"""
Project NEXUS
Vision Tool

Vision Foundation v1 + Vision Semantic Layer v2.
"""

from __future__ import annotations

from pathlib import Path
import colorsys

from nexus.tools.base_tool import BaseTool


class VisionTool(BaseTool):
    """Analyzes local image files safely."""

    name = "vision"
    description = "画像の安全確認・基礎分析・意味分析を行います"

    def __init__(self) -> None:
        self.allowed_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".bmp",
            ".gif",
            ".tif",
            ".tiff",
        }
        self.max_size_mb = 25

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text.startswith("画像分析:")
            or text.startswith("画像分析：")
            or text.startswith("画像意味分析:")
            or text.startswith("画像意味分析：")
            or text.startswith("画像安全確認:")
            or text.startswith("画像安全確認：")
            or text == "画像ヘルプ"
            or text == "vision help"
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text in {"画像ヘルプ", "vision help"}:
            return self._help()

        if text.startswith(("画像安全確認:", "画像安全確認：")):
            path = self._extract_path(text)
            return self._safety_check(path)

        if text.startswith(("画像分析:", "画像分析：")):
            path = self._extract_path(text)
            return self._analyze(path)

        if text.startswith(("画像意味分析:", "画像意味分析：")):
            path = self._extract_path(text)
            return self._semantic_analyze(path)

        return "対応していない画像操作です。"

    def _extract_path(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip().strip('"').strip("'")
        return ""

    def _resolve_path(self, path_text: str) -> Path:
        return Path(path_text).expanduser().resolve()

    def _basic_file_check(self, path_text: str) -> tuple[bool, str, Path | None]:
        if not path_text:
            return False, "画像ファイルのパスがありません。", None

        path = self._resolve_path(path_text)

        if not path.exists():
            return False, f"ファイルが見つかりません: {path}", path

        if not path.is_file():
            return False, f"ファイルではありません: {path}", path

        if path.suffix.lower() not in self.allowed_extensions:
            return (
                False,
                f"対応していない拡張子です: {path.suffix}\n"
                f"対応: {', '.join(sorted(self.allowed_extensions))}",
                path,
            )

        size_mb = path.stat().st_size / (1024 * 1024)

        if size_mb > self.max_size_mb:
            return (
                False,
                f"ファイルが大きすぎます: {size_mb:.2f}MB\n"
                f"上限: {self.max_size_mb}MB",
                path,
            )

        return True, "基本チェックOK", path

    def _safety_check(self, path_text: str) -> str:
        ok, message, path = self._basic_file_check(path_text)

        if not ok:
            return f"## Image Safety Check\n\nResult: blocked\nReason: {message}"

        try:
            from PIL import Image

            assert path is not None

            with Image.open(path) as image:
                image.verify()

            size_mb = path.stat().st_size / (1024 * 1024)

            return (
                "## Image Safety Check\n\n"
                "Result: allowed\n"
                f"File: {path}\n"
                f"Size: {size_mb:.2f}MB\n"
                f"Extension: {path.suffix.lower()}\n\n"
                "Notes:\n"
                "- 画像として開けることを確認しました。\n"
                "- この確認はウイルス完全検出ではありません。\n"
                "- 自動実行・外部送信はしません。"
            )

        except Exception as error:
            return (
                "## Image Safety Check\n\n"
                "Result: blocked\n"
                f"File: {path}\n"
                f"Reason: 画像として検証できませんでした: {error}"
            )

    def _analyze(self, path_text: str) -> str:
        ok, message, path = self._basic_file_check(path_text)

        if not ok:
            return f"## Vision Analysis\n\n分析できません。\nReason: {message}"

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

            orientation = self._orientation(width, height)
            hints = self._visual_hints(mean_rgb, brightness, contrast, saturation)

            return (
                "## Vision Analysis\n\n"
                f"File: {path}\n"
                f"Format: {original_format}\n"
                f"Mode: {mode}\n"
                f"Size: {width} x {height}px\n"
                f"Orientation: {orientation}\n\n"
                "### Basic Metrics\n"
                f"- Brightness: {brightness:.1f} / 255\n"
                f"- Contrast: {contrast:.1f}\n"
                f"- Saturation: {saturation:.1f} / 100\n\n"
                "### Dominant Colors\n"
                + "\n".join(f"- RGB{color}" for color in dominant)
                + "\n\n"
                "### Visual Hints\n"
                + "\n".join(f"- {hint}" for hint in hints)
                + "\n\n"
                "### Limits\n"
                "- これは基礎画像分析です。\n"
                "- 物体名・植物名・鉱物名の確定識別はまだ行いません。\n"
                "- 画像意味分析で、もう少し意味寄りの推定ができます。"
            )

        except Exception as error:
            return f"画像分析に失敗しました: {error}"

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
                score_lines.append(f"- {label}: {score:3d}/100 {self._score_bar(score)}")

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
                f"- Color Variety: {color_variety:.1f}\n\n"
                "### Dominant Colors\n"
                + "\n".join(f"- RGB{color}" for color in dominant)
                + "\n\n"
                "### Limits\n"
                "- これはローカル特徴量による意味推定です。\n"
                "- 物体名・植物名・鉱物名は断定しません。\n"
                "- 人物の個人特定はしません。\n"
                "- 本格的な画像認識AIではなく、意味分析層です。"
            )

        except Exception as error:
            return f"画像意味分析に失敗しました: {error}"

    def _average_saturation(self, image) -> float:
        pixels = list(image.resize((64, 64)).getdata())
        values = []

        for r, g, b in pixels:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            values.append(s * 100)

        if not values:
            return 0.0

        return sum(values) / len(values)

    def _dominant_colors(self, image) -> list[tuple[int, int, int]]:
        small = image.resize((80, 80)).convert("RGB")

        try:
            quantized = small.quantize(colors=5)
            palette = quantized.getpalette()
            color_counts = quantized.getcolors()

            if not color_counts or not palette:
                return []

            color_counts.sort(reverse=True)
            colors = []

            for count, index in color_counts[:5]:
                base = index * 3
                colors.append(
                    (
                        palette[base],
                        palette[base + 1],
                        palette[base + 2],
                    )
                )

            return colors

        except Exception:
            return []

    def _orientation(self, width: int, height: int) -> str:
        if width == height:
            return "square"

        ratio = width / height

        if ratio > 1.2:
            return "landscape"

        if ratio < 0.8:
            return "portrait"

        return "near-square"

    def _visual_hints(
        self,
        mean_rgb: list[float],
        brightness: float,
        contrast: float,
        saturation: float,
    ) -> list[str]:
        r, g, b = mean_rgb
        hints: list[str] = []

        if brightness < 45:
            hints.append("全体的に暗い画像です。照明不足か夜景の可能性があります。")
        elif brightness > 210:
            hints.append("全体的に明るい画像です。白背景・強い光・露出高めの可能性があります。")
        else:
            hints.append("明るさは極端ではありません。")

        if contrast < 25:
            hints.append("コントラストは低めです。平坦・ぼやけ・均一な面が多い可能性があります。")
        elif contrast > 70:
            hints.append("コントラストは高めです。強い陰影や輪郭がある可能性があります。")
        else:
            hints.append("コントラストは中程度です。")

        if saturation < 18:
            hints.append("彩度が低いです。金属・石・紙・白黒に近い対象の可能性があります。")
        elif saturation > 55:
            hints.append("彩度が高めです。人工物・花・鮮やかな素材などの可能性があります。")
        else:
            hints.append("彩度は中程度です。")

        if g > r * 1.15 and g > b * 1.15 and saturation > 25:
            hints.append("緑成分が強いです。植物・草・自然物が写っている可能性があります。")

        if abs(r - g) < 15 and abs(g - b) < 15 and saturation < 20:
            hints.append("RGB差が小さく低彩度です。石・鉱物・金属・コンクリート系の可能性があります。")

        if contrast > 45 and saturation < 35:
            hints.append("輪郭や陰影があり低彩度です。人工物や硬い素材の可能性もあります。")

        return hints

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
        plant += 10 if 55 < brightness < 210 else 0
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
        photo += 15 if 20 < contrast < 75 else 0
        photo += 15 if 10 < saturation < 70 else 0
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

    def _help(self) -> str:
        return (
            "## Vision Tool Help\n\n"
            "使えるコマンド:\n"
            "- 画像安全確認: /path/to/image.png\n"
            "- 画像分析: /path/to/image.png\n"
            "- 画像意味分析: /path/to/image.png\n\n"
            "例:\n"
            "- 画像分析: tests/assets/sample_vision.png\n"
            "- 画像意味分析: tests/assets/sample_vision.png\n\n"
            "現在できること:\n"
            "- 画像形式・サイズ確認\n"
            "- 明るさ・コントラスト・彩度\n"
            "- 支配色\n"
            "- 植物/鉱物/人工物っぽさの簡易ヒント\n"
            "- 意味分析: 植物/鉱物/人工物/イラスト/写真/背景っぽさのスコア\n\n"
            "まだできないこと:\n"
            "- 正確な物体認識\n"
            "- 植物名・鉱物名の確定\n"
            "- 人物の個人特定\n"
            "- ライブカメラ解析\n"
        )
