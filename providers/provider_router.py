from providers.abstract_ai_provider import AbstractAIProvider
from .gemini import GeminiProvider
from .openai import OpenAIProvider


class ProviderRouter:
  def __init__(self):
    self._openai_provider = OpenAIProvider()
    self._gemini_provider = GeminiProvider()

  def route_to_ai_provider(self, model_name) -> AbstractAIProvider:
    if model_name in ["gpt-4o-mini", "gpt-4o", "o1-mini"]:
      return self._openai_provider
    if model_name in ["gemini-1.5-flash"]:
      return self._gemini_provider