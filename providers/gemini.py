from conversation import Conversation
from providers.abstract_ai_provider import AbstractAIProvider

from google.generativeai import protos
import google.generativeai as genai


class GeminiProvider(AbstractAIProvider):
    def send_user_message(self, content, current_convo=Conversation(model="gemini-1.5-flash")):
      prompt_history = []
      for msg in current_convo.messages:
        role = 'model' if msg['role'] == 'assistant' else msg['role']
        prompt_history.append(protos.Content(role=role, parts=protos.Part(text=msg['content'])))
      model = genai.GenerativeModel('gemini-1.5-flash')
      chat = genai.ChatSession(model=model, history=prompt_history)
      response = chat.send_message(content)
      return {"role": "assistant", "content": response.text}


if __name__ == '__main__':
  print( GeminiProvider().send_user_message("Write back: abc") )
