from conversation import Message, Conversation
from providers.abstract_ai_provider import AbstractAIProvider

import os
from openai import OpenAI


class OpenAIProvider(AbstractAIProvider):
  def __init__(self):
    self.client: OpenAI = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

  def send_user_message(self, content: str, current_convo : Conversation = Conversation(model="gpt-4o-mini")):
    new_msg = {'role': 'user', 'content': content}
    chat_completion = self.client.chat.completions.create(
         messages=current_convo.messages + [new_msg],
         model=current_convo.model,
    )
    message = chat_completion.choices[0].message
    assert message.role == 'assistant'
    return {"role": message.role, "content": message.content}

