from typing import List, TypedDict

from dataclasses import dataclass


class Message(TypedDict):
  role: str
  content: str


class Conversation:
  """ A single conversation (chat with history), to accomplish a single task
  """

  def __init__(self, initial_messages: List[Message] = [], model: str = "gpt-4o"):
    self.model = model
    self.messages: List[Message] = initial_messages

  def add_message(self, msg: Message):
    self.messages.append(msg)

