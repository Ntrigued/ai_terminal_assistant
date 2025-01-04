from abc import ABC, abstractmethod

from conversation import Message


class AbstractAIProvider(ABC):
    """Abstract base class for AI providers."""
    @abstractmethod
    def send_user_message(self, message) -> Message:
        """Send a user message to the AI provider."""
        pass
