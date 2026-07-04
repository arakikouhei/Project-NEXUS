"""
Project NEXUS
Context Builder
"""


class ContextBuilder:
    """Builds the current execution context."""

    def build(self) -> dict:
        """Return the current context."""

        return {
            "project": "Project NEXUS",
            "last_file": None,
            "last_tool": None,
            "last_task": None,
        }