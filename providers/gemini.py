from conversation import Conversation
from providers.abstract_ai_provider import AbstractAIProvider

from google.generativeai import protos
import google.generativeai as genai


class GeminiProvider(AbstractAIProvider):
    def send_user_message(self, content, current_convo=Conversation(model="gemini-1.5-flash")):
      if content == "":
        content = " "
      prompt_history = []
      for msg in current_convo.messages:
        role = 'model' if msg['role'] in ['assistant', 'system'] else msg['role']
        prompt_history.append(protos.Content(role=role, parts=[protos.Part(text=msg['content'])]))
      model = genai.GenerativeModel('gemini-1.5-flash')
      chat = genai.ChatSession(model=model, history=prompt_history)
      response = chat.send_message(content)
      return {"role": "assistant", "content": response.text}
