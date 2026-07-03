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
        keywords = [
            "どこ",
            "探して",
            "検索",
            "ファイル",
        ]

        return any(word in user_input for word in keywords)

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