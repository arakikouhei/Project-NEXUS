"""
Project NEXUS
Tool Manager
"""

from nexus.tools.base_tool import BaseTool
from nexus.tools.clock import ClockTool
from nexus.tools.git import GitTool
from nexus.tools.terminal import TerminalTool
from nexus.tools.context import ContextTool
from nexus.tools.system import SystemTool
from nexus.tools.voice import VoiceTool
from nexus.tools.test import TestTool
from nexus.tools.dashboard import DashboardTool
from nexus.tools.worklog import WorkLogTool
from nexus.tools.hardware import HardwareTool
from nexus.tools.capability import CapabilityTool
from nexus.tools.transfer import TransferTool
from nexus.tools.diagnostics import ToolDiagnosticsTool
from nexus.tools.backup_export import BackupExportTool
from nexus.tools.command_help import CommandHelpTool
from nexus.tools.project_memory import ProjectMemoryTool
from nexus.tools.knowledge_import import KnowledgeImportTool
from nexus.tools.research_workflow import ResearchWorkflowTool
from nexus.tools.memory_index import MemoryIndexTool
from nexus.tools.work_notes import WorkNotesTool
from nexus.tools.memory_review import MemoryReviewTool
from nexus.tools.memory_answer import MemoryAnswerTool
from nexus.tools.web import WebTool
from nexus.tools.research import SafeResearchTool
from nexus.tools.safe_search import SafeSearchTool
from nexus.tools.vision import VisionTool
from nexus.tools.vision_memory import VisionMemoryTool
from nexus.tools.knowledge import KnowledgeTool
from nexus.tools.source_registry import SourceRegistryTool
from nexus.tools.world_update import WorldUpdateTool
from nexus.tools.paper_intake import PaperIntakeTool
from nexus.tools.app import AppControlTool
from nexus.tools.math import AdvancedMathTool
from nexus.tools.calculator import CalculatorTool
from nexus.tools.filesystem import FileSystemTool
from nexus.tools.project import ProjectTool
from nexus.tools.code import CodeTool


class ToolManager:
    """Manages all tools."""

    def __init__(self) -> None:
        self.tools: list[BaseTool] = []

        # Core / status tools
        self.register(ClockTool())
        self.register(GitTool())
        self.register(TerminalTool())
        self.register(ContextTool())
        self.register(SystemTool())
        self.register(VoiceTool())
        self.register(TestTool())
        self.register(DashboardTool())
        self.register(WorkLogTool())
        self.register(HardwareTool())

        # Specific command tools must come before broad/help/math tools.
        self.register(ToolDiagnosticsTool())
        self.register(BackupExportTool())
        self.register(CommandHelpTool())
        self.register(ProjectMemoryTool())
        self.register(KnowledgeImportTool())
        self.register(ResearchWorkflowTool())
        self.register(MemoryIndexTool())
        self.register(WorkNotesTool())
        self.register(MemoryReviewTool())
        self.register(MemoryAnswerTool())
        self.register(TransferTool())
        self.register(SafeSearchTool())
        self.register(SafeResearchTool())
        self.register(WebTool())
        self.register(VisionTool())
        self.register(VisionMemoryTool())
        self.register(KnowledgeTool())
        self.register(SourceRegistryTool())
        self.register(WorldUpdateTool())
        self.register(PaperIntakeTool())
        self.register(AppControlTool())

        # Math tools must come before general calculator, but after specific tools.
        self.register(AdvancedMathTool())
        self.register(CalculatorTool())

        # Broad/help tools should come after specific tools.
        self.register(CapabilityTool())

        # Project/code tools
        self.register(FileSystemTool())
        self.register(ProjectTool())
        self.register(CodeTool())

    def register(self, tool: BaseTool) -> None:
        self.tools.append(tool)

    def execute(self, user_input: str) -> str | None:
        for tool in self.tools:
            if tool.can_handle(user_input):
                return tool.execute(user_input)

        return None
