"""
memory.py — Simple In-Memory Storage for Conversation History

=== ADK CONCEPT: MEMORY ===
Memory in ADK refers to the ability of an agent to recall information
from past interactions. While ADK provides built-in session history,
this module demonstrates a CUSTOM memory layer — a simple dictionary-based
store that persists conversation history across the session.

This is useful for:
- Personalizing responses based on past topics
- Tracking what the user has asked before
- Building context awareness over time

In production, you'd replace this with a database or ADK's MemoryService.
"""


class ConversationMemory:
    """
    A simple in-memory store for conversation history.
    
    Stores past user queries and agent responses as a list of dictionaries.
    This acts as the agent's "long-term memory" within a single run.
    
    ADK NOTE: ADK also provides a MemoryService for production use cases
    (e.g., searching past sessions). This is a simplified, educational version.
    """

    def __init__(self):
        # The core memory store — a list of conversation turns
        self._history: list[dict] = []
        # Track unique topics the user has asked about
        self._topics: list[str] = []

    def add_turn(self, user_query: str, agent_response: str) -> None:
        """
        Store a single conversation turn (user input + agent response).
        
        Args:
            user_query: What the user said
            agent_response: What the agent replied
        """
        self._history.append({
            "user": user_query,
            "agent": agent_response
        })

    def add_topic(self, topic: str) -> None:
        """Track a topic the user has discussed."""
        if topic not in self._topics:
            self._topics.append(topic)

    def get_history(self) -> list[dict]:
        """Return the full conversation history."""
        return self._history

    def get_recent_history(self, n: int = 3) -> list[dict]:
        """
        Get the last N conversation turns.
        
        Useful for injecting recent context into the agent's prompt
        without overwhelming it with the entire history.
        """
        return self._history[-n:]

    def get_topics(self) -> list[str]:
        """Return all unique topics discussed so far."""
        return self._topics

    def get_summary(self) -> str:
        """
        Generate a brief summary of the conversation so far.
        This can be injected into the agent prompt for personalization.
        """
        if not self._history:
            return "No previous conversation."

        total = len(self._history)
        topics_str = ", ".join(self._topics) if self._topics else "general chat"
        return (
            f"The user has asked {total} question(s) so far. "
            f"Topics discussed: {topics_str}."
        )
