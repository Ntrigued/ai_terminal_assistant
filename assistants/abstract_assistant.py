from typing import Optional

from openai import OpenAI
import os
import subprocess
import sys
from conversation import Message, Conversation
from prompts import BASE_PROMPT


class AbstractAssistant:
  def __init__(self, starter_prompt, model="gpt-4o-mini"):
    self.client: OpenAI = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    self.current_convo: Conversation = Conversation(initial_messages=starter_prompt, model=model)

  def _command(self, command) -> str:
    """ Allow the assistant to execute commands
    """
    if 'mv' in command or 'rm' in command:
      print(f"Assistant wants to run the command: {command}")
      resp = input("Allow (Y/N)?: ")
      if resp.upper() == 'N':
        return "User refused to allow command to be run"
      if resp.upper() != "Y":
        print("Must be one of 'Y' or 'N'")
        return self._command(command)
    print(f"Running command: {command}")
    command = f"timeout 60s {command}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Command output: {result.stdout}")
    return result.stdout.strip()


  def _send_message(self, role, content) -> Message:
    user_msg: Message = {"role": role, "content": content}
    try:
      chat_completion = self.client.chat.completions.create(
          messages=self.current_convo.messages + [user_msg],
           model=self.current_convo.model,
      )
      message = chat_completion.choices[0].message
      assert message.role == 'assistant'
    except Exception as e:
      error_msg = "There was an error handling your query and it hasn't been added to the conversation: {e}"
      # Don't run current_convo.add_message for this,
      # we don't want the assistant to reference it in the future
      return {'role': 'assistant', 'content': error_msg}
    else:
      self.current_convo.add_message(user_msg)
      self.current_convo.add_message({"role": message.role, "content": message.content})
      return {"role": message.role, "content": message.content}

