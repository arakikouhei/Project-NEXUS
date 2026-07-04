"""
Project NEXUS
Project Tool
"""

from nexus.project.code_index import CodeIndex
from nexus.project.index import ProjectIndex
from nexus.tools.base_tool import BaseTool


class ProjectTool(BaseTool):
    """Search project files and code."""

    name = "project"
    description = "プロジェクト内のファイルやコードを検索します"

    def __init__(self) -> None:
        self.index = ProjectIndex()
        self.code_index = CodeIndex()

    def can_handle(self, user_input: str) -> bool:
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

        return any(word in text for word in keywords)
    def execute(self, user_input: str) -> str:
        keyword = user_input

        for word in ["どこ", "探して", "検索", "ファイル", "は", "？", "?"]:
            keyword = keyword.replace(word, "")

        keyword = keyword.strip()

        if not keyword:
            return "検索するキーワードを指定してください。"

        file_results = self.index.search(keyword)

        if file_results:
            return "\n".join(file_results[:20])

        code_results = self.code_index.search(keyword)

        if code_results:
            return "\n".join(code_results[:20])

        return f"{keyword} に一致するファイルやコードは見つかりませんでした。"
