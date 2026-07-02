"""
Project NEXUS
Conversation Memory
"""


class ConversationMemory:
    """Stores recent conversation history."""

    def __init__(self, max_history: int = 10) -> None:
        self.max_history = max_history
        self.history = []

    def add(self, role: str, content: str) -> None:
        """Add a message to history."""

        self.history.append({
            "role": role,
            "content": content,
        })

        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_history(self) -> list:
        """Return conversation history."""
        return self.history

    def clear(self) -> None:
        """Clear conversation history."""
        self.history.clear()