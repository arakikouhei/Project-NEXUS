"""
Project NEXUS
Simple Planner
"""


class SimplePlanner:
    """Creates simple plans for user requests."""

    def plan(self, user_input: str) -> list[str]:
        steps = []

        if "コミット" in user_input:
            steps.append("Check Git status")
            steps.append("Review changes")
            steps.append("Commit safely")

        elif "解析" in user_input:
            steps.append("Find target file")
            steps.append("Analyze code")
            steps.append("Summarize result")

        elif "状況" in user_input:
            steps.append("Build current context")
            steps.append("Summarize project state")

        else:
            steps.append("Decide whether a tool can handle the request")
            steps.append("Use AI response if no tool matches")

        return steps
