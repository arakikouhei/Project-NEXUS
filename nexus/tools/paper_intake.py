"""
Project NEXUS
Paper Intake Tool v1

Safe arXiv metadata intake.
This tool stores metadata and summaries, not bulk PDFs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import unescape
import re
import ssl
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    import certifi
except Exception:
    certifi = None

from nexus.memory.knowledge_store import KnowledgeStore
from nexus.tools.base_tool import BaseTool


@dataclass(frozen=True)
class ArxivPaper:
    arxiv_id: str
    title: str
    authors: list[str]
    summary: str
    published: str
    updated: str
    categories: list[str]
    link: str
    pdf_url: str


class PaperIntakeTool(BaseTool):
    """Searches and stores safe paper metadata from arXiv."""

    name = "paper_intake"
    description = "arXivから安全に論文メタ情報・要約を取り込みます"

    def __init__(self) -> None:
        self.knowledge = KnowledgeStore()
        self.last_results: list[ArxivPaper] = []
        self.max_results = 5

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text == "論文ヘルプ"
            or text == "論文一覧"
            or text.startswith("論文検索:")
            or text.startswith("論文検索：")
            or text.startswith("論文保存:")
            or text.startswith("論文保存：")
            or text.startswith("論文詳細:")
            or text.startswith("論文詳細：")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "論文ヘルプ":
            return self._help()

        if text == "論文一覧":
            return self._list_papers()

        if text.startswith(("論文検索:", "論文検索：")):
            query = self._after_separator(text)
            return self._search(query)

        if text.startswith(("論文保存:", "論文保存：")):
            paper_id = self._after_separator(text)
            return self._save_paper(paper_id)

        if text.startswith(("論文詳細:", "論文詳細：")):
            entry_id = self._after_separator(text)
            return self._detail(entry_id)

        return "対応していない論文操作です。"

    def _after_separator(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip()
        return ""

    def _search(self, query: str) -> str:
        if not query:
            return "検索語がありません。例: 論文検索: computer graphics"

        try:
            papers = self._arxiv_search(query, max_results=self.max_results)
        except Exception as error:
            return (
                "## Paper Search Failed\n\n"
                f"Query: {query}\n"
                f"Reason: {error}\n\n"
                "ネット接続、SSL、またはarXiv API応答の問題の可能性があります。"
            )

        self.last_results = papers

        if not papers:
            return f"## Paper Search\n\nQuery: {query}\n\n該当する論文が見つかりませんでした。"

        lines = [
            "## Paper Search / arXiv",
            "",
            f"Query: {query}",
            "",
        ]

        for index, paper in enumerate(papers, start=1):
            lines.append(f"### {index}. {paper.title}")
            lines.append(f"- arXiv ID: {paper.arxiv_id}")
            lines.append(f"- Authors: {', '.join(paper.authors[:5])}")
            lines.append(f"- Published: {paper.published}")
            lines.append(f"- Categories: {', '.join(paper.categories)}")
            lines.append(f"- URL: {paper.link}")
            brief = paper.summary
            if len(brief) > 450:
                brief = brief[:450].rstrip() + "..."
            lines.append("")
            lines.append(brief)
            lines.append("")
            lines.append(f"保存するなら: 論文保存: {paper.arxiv_id}")
            lines.append("")

        lines.append("Notes:")
        lines.append("- v1はarXivのメタ情報と要約のみ扱います。")
        lines.append("- PDFの大量保存や全文学習はしません。")
        lines.append("- 内容の正確性確認には原文確認が必要です。")

        return "\n".join(lines).rstrip()

    def _save_paper(self, paper_id: str) -> str:
        if not paper_id:
            return "論文IDがありません。例: 論文保存: 2501.00001"

        paper = self._find_last_result(paper_id)

        if paper is None:
            try:
                papers = self._arxiv_by_id(paper_id)
            except Exception as error:
                return f"論文取得に失敗しました: {error}"

            if not papers:
                return f"論文が見つかりませんでした: {paper_id}"

            paper = papers[0]

        content = self._paper_to_knowledge_content(paper)

        try:
            entry = self.knowledge.add(
                category="papers",
                content=content,
                source="arxiv",
                tags=[
                    "arxiv",
                    paper.arxiv_id,
                    *paper.categories[:5],
                    *self._tag_words(paper.title)[:8],
                ],
            )
        except Exception as error:
            return f"論文保存に失敗しました: {error}"

        return (
            "## Paper Saved\n\n"
            f"- Knowledge ID: {entry.get('id')}\n"
            f"- arXiv ID: {paper.arxiv_id}\n"
            f"- Title: {paper.title}\n"
            f"- Category: papers\n"
            f"- URL: {paper.link}\n\n"
            "保存した内容は `知識検索:` で検索できます。"
        )

    def _list_papers(self) -> str:
        papers = self.knowledge.list_entries(category="papers", limit=20)

        if not papers:
            return "## Paper List\n\nまだ論文知識は保存されていません。"

        lines = ["## Paper List", ""]

        for item in papers:
            content = item.get("content", "")
            title = self._extract_field(content, "Title") or content[:80]
            lines.append(f"### {item.get('id')}")
            lines.append(f"- Created: {item.get('created_at')}")
            lines.append(f"- Source: {item.get('source')}")
            lines.append(f"- Title: {title}")
            lines.append(f"- Tags: {', '.join(item.get('tags', []))}")
            lines.append("")

        return "\n".join(lines).rstrip()

    def _detail(self, entry_id: str) -> str:
        if not entry_id:
            return "IDがありません。例: 論文詳細: papers-xxxxxxxx"

        item = self.knowledge.get(entry_id)

        if not item or item.get("category") != "papers":
            return f"論文知識IDが見つかりません: {entry_id}"

        return (
            "## Paper Detail\n\n"
            f"- Knowledge ID: {item.get('id')}\n"
            f"- Source: {item.get('source')}\n"
            f"- Created: {item.get('created_at')}\n"
            f"- Tags: {', '.join(item.get('tags', []))}\n\n"
            f"{item.get('content')}"
        )

    def _arxiv_search(self, query: str, max_results: int = 5) -> list[ArxivPaper]:
        safe_query = self._build_search_query(query)
        params = urlencode(
            {
                "search_query": safe_query,
                "start": 0,
                "max_results": max_results,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )

        url = f"https://export.arxiv.org/api/query?{params}"
        return self._fetch_arxiv(url)

    def _arxiv_by_id(self, paper_id: str) -> list[ArxivPaper]:
        clean_id = paper_id.strip()
        params = urlencode(
            {
                "id_list": clean_id,
                "start": 0,
                "max_results": 1,
            }
        )

        url = f"https://export.arxiv.org/api/query?{params}"
        return self._fetch_arxiv(url)

    def _fetch_arxiv(self, url: str) -> list[ArxivPaper]:
        request = Request(
            url,
            headers={
                "User-Agent": "Project-NEXUS-PaperIntake/0.1",
            },
        )

        with urlopen(request, timeout=15, context=self._ssl_context()) as response:
            raw = response.read(1_500_000)

        root = ET.fromstring(raw)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }

        papers: list[ArxivPaper] = []

        for entry in root.findall("atom:entry", ns):
            title = self._clean(self._text(entry, "atom:title", ns))
            summary = self._clean(self._text(entry, "atom:summary", ns))
            published = self._text(entry, "atom:published", ns)
            updated = self._text(entry, "atom:updated", ns)
            link = self._entry_link(entry, ns)
            pdf_url = self._pdf_link(entry, ns)
            arxiv_id = self._extract_arxiv_id(self._text(entry, "atom:id", ns))

            authors = []
            for author in entry.findall("atom:author", ns):
                name = self._text(author, "atom:name", ns)
                if name:
                    authors.append(self._clean(name))

            categories = []
            for category in entry.findall("atom:category", ns):
                term = category.attrib.get("term")
                if term:
                    categories.append(term)

            if title and arxiv_id:
                papers.append(
                    ArxivPaper(
                        arxiv_id=arxiv_id,
                        title=title,
                        authors=authors,
                        summary=summary,
                        published=published,
                        updated=updated,
                        categories=categories,
                        link=link or f"https://arxiv.org/abs/{arxiv_id}",
                        pdf_url=pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
                    )
                )

        return papers

    def _build_search_query(self, query: str) -> str:
        # all: はarXiv APIの検索対象全体。v1では安全にall検索だけ。
        cleaned = query.strip().replace('"', " ")
        cleaned = re.sub(r"\s+", " ", cleaned)
        terms = [term for term in cleaned.split(" ") if term]

        if not terms:
            return "all:"

        if len(terms) == 1:
            return f"all:{terms[0]}"

        return " AND ".join(f"all:{term}" for term in terms[:6])

    def _find_last_result(self, paper_id: str) -> ArxivPaper | None:
        target = paper_id.strip().lower()

        for paper in self.last_results:
            if paper.arxiv_id.lower() == target:
                return paper

        return None

    def _paper_to_knowledge_content(self, paper: ArxivPaper) -> str:
        now = datetime.now().isoformat(timespec="seconds")

        return (
            f"Paper Source: arXiv\n"
            f"arXiv ID: {paper.arxiv_id}\n"
            f"Title: {paper.title}\n"
            f"Authors: {', '.join(paper.authors)}\n"
            f"Published: {paper.published}\n"
            f"Updated: {paper.updated}\n"
            f"Categories: {', '.join(paper.categories)}\n"
            f"URL: {paper.link}\n"
            f"PDF URL: {paper.pdf_url}\n"
            f"Fetched At: {now}\n"
            f"\nAbstract:\n{paper.summary}\n\n"
            "NEXUS Note:\n"
            "- v1ではメタ情報とAbstractのみ保存。\n"
            "- 内容の理解・評価・再現性確認には原文確認が必要。\n"
            "- ライセンスや利用条件に注意。"
        )

    def _entry_link(self, entry, ns: dict) -> str:
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("rel") == "alternate":
                return link.attrib.get("href", "")
        return ""

    def _pdf_link(self, entry, ns: dict) -> str:
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("title") == "pdf":
                return link.attrib.get("href", "")
        return ""

    def _extract_arxiv_id(self, text: str) -> str:
        text = text.strip()
        if "/" in text:
            return text.rsplit("/", 1)[-1]
        return text

    def _text(self, element, path: str, ns: dict) -> str:
        found = element.find(path, ns)
        if found is None or found.text is None:
            return ""
        return found.text

    def _clean(self, text: str) -> str:
        text = unescape(text or "")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _tag_words(self, text: str) -> list[str]:
        words = re.findall(r"[A-Za-z][A-Za-z0-9_+\-.#]*|[一-龥ぁ-んァ-ン]{2,}", text)
        result = []

        for word in words:
            if word not in result:
                result.append(word)
            if len(result) >= 12:
                break

        return result

    def _extract_field(self, content: str, field: str) -> str:
        prefix = f"{field}:"
        for line in content.splitlines():
            if line.startswith(prefix):
                return line[len(prefix):].strip()
        return ""

    def _ssl_context(self) -> ssl.SSLContext:
        if certifi is not None:
            return ssl.create_default_context(cafile=certifi.where())
        return ssl.create_default_context()

    def _help(self) -> str:
        return (
            "## Paper Intake Help\n\n"
            "使えるコマンド:\n"
            "- 論文検索: artificial intelligence\n"
            "- 論文検索: computer graphics\n"
            "- 論文保存: 2501.00001\n"
            "- 論文一覧\n"
            "- 論文詳細: papers-xxxxxxxx\n\n"
            "v1の対象:\n"
            "- arXiv API\n"
            "- タイトル\n"
            "- 著者\n"
            "- Abstract\n"
            "- 公開日/更新日\n"
            "- URL\n"
            "- arXivカテゴリ\n\n"
            "やらないこと:\n"
            "- PDF大量保存\n"
            "- 全文の無断再配布\n"
            "- 論文内容の正しさの断定\n\n"
            "保存先:\n"
            "- Knowledge Core / papers"
        )
