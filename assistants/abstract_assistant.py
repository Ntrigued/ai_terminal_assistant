import traceback
from typing import Optional
from openai import OpenAI
import os
import subprocess
import sys

from conversation import Message, Conversation
from prompts import BASE_PROMPT
from providers.abstract_ai_provider import AbstractAIProvider
from providers.provider_router import ProviderRouter


class AbstractAssistant:
  def __init__(self, starter_prompt, model="gpt-4o-mini"):
    self.client: OpenAI = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    self.current_convo: Conversation = Conversation(initial_messages=starter_prompt, model=model)
    self.provider_router = ProviderRouter()

  def _command(self, command) -> str:
    """ Allow the assistant to execute commands
    """
    if command.startswith('cd'):
      new_dir = command.replace('cd', '').strip()
      try:
         os.chdir(new_dir)
         print(f"Command Output: directory changed to: {os.getcwd()}")
         return f"directory changed to: {os.getcwd()}"
      except:
         err_msg = f"Can't run this command to change directory: <command>{command}</command>. "\
                   "It may include more than just a 'cd' "\
                   "(such as if its chained with another command"
         print(f"Command output: {err_msg}", file=sys.stderr)
         return err_msg
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
    print(f"Command output: stdout: {result.stdout} stderr: {result.stderr}")
    if result.stderr.strip():
      print(f"Command output (Error): {result.stderr}", file=sys.stderr)
      return result.stderr.strip()
    print(f"Command output: {result.stdout}")
    return result.stdout.strip()


  def _send_user_message(self, content) -> Message:
    try:
      user_msg: Message = {"role": "user", "content": content}
      ai_provider: AbstractAIProvider  = self.provider_router.route_to_ai_provider(self.current_convo.model)
      assistant_message = ai_provider.send_user_message(content, self.current_convo)
      self.current_convo.add_message(user_msg)
      self.current_convo.add_message(assistant_message)
      return assistant_message
    except Exception as e:
      error_msg = f"There was an error handling your query and it hasn't been added to the conversation: {e}"
      traceback.print_exc()
      # Don't run current_convo.add_message for this,
      # we don't want the assistant to reference it in the future
      return {'role': 'assistant', 'content': error_msg}
