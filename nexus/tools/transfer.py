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
