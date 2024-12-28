from typing import Optional

from openai import OpenAI
import os
import subprocess
import sys
from conversation import Message, Conversation
from prompts import BASE_PROMPT
from .abstract_assistant import AbstractAssistant
from .code_assistant import CodeAssistant


class BaseAssistant(AbstractAssistant):
  def __init__(self, starter_prompt=BASE_PROMPT()):
    super().__init__(starter_prompt=BASE_PROMPT())
    self.mode = 'Standard'

  def interaction_loop(self):
    print(f"{self.mode} Assistant: What can I help you with?")
    while True:
      self.query_user()

  def query_user(self, user_query=None):
    if not user_query:
      user_query = input("User: ")
    user_query = user_query.strip()
    if user_query.lower() == 'exit assistant':
      sys.exit(0)
    elif user_query.lower() == 'new convo':
       self.current_convo = Conversation(initial_messages=BASE_PROMPT(), model='gpt-4o-mini')
       print(f"{self.mode} Assistant: conversation was reset")
    elif user_query.lower() == 'think hard':
       self.mode = "Genius"
       print(f"{self.mode} Assistant: Activating genius mode!")
    elif user_query.lower() == 'think super hard':
       self.mode = "Einstein"
       print(f"{self.mode} Assistant: Activating Einstein mode!")
    elif user_query.lower() == "think cheap":
       self.mode = "Standard"
       print(f"{self.mode} Assistant: Brain size shrinking :(")
    elif self.mode in ['Genius', 'Einstein']:
       self.current_convo.model = 'o1-mini'
       self.current_convo.messages[0]['role'] = 'user'

       assistant_response = self._send_message(role="user", content="Write a plan for yourself (as the AI assistant who only has access to the terminal "+
                                                "commands I've told you about) to solve the following task or query. THE PLAN NEEDS TO SOLVE IT EXACTLY AS DEFINED, DON'T "+
                                                "ADD ANY IMPROVEMENTS OR OPTIONAL STEPS:\n\n" + user_query)
       print(f"o1-mini plan: {assistant_response}")
       self.current_convo.model = 'gpt-4o-mini'
       self.current_convo.messages[0]['role'] = 'system'
       if self.mode == 'Einstein':
         self.current_convo.model = 'gpt-4o'
       self._respond_to_query("Now follow the plan you've created.")
    else:
       self._respond_to_query(user_query)

  def _respond_to_query(self, user_query: str) -> bool:
    assistant_response = self._send_message(role="user", content=user_query)["content"]
    while True:
      if '<command>' in assistant_response.lower():
        resp_lower = assistant_response.lower()
        command = assistant_response[resp_lower.find('<command>')+len('<command>'):resp_lower.find('</command>')]
        chain_of_thought = assistant_response.replace(f'<command>{command}</command>', '')
        print(f'Chain of Thought: {chain_of_thought}')
        if command.startswith('cd'):
          new_dir = command.replace('cd', '').strip()
          os.chdir(new_dir)
        if 'code_assistant' in command:
          print(f"command: {command}")
          CodeAssistant(chain_of_thought).interaction_loop()
          assistant_response = self._send_message(role="user", content="The coding assistant has handled your request! Continue as if the task is completed (and don't reference this message).")
        else:
          command_output = self._command(command)
          #print(f'Command Output:\n{command_output}')
          assistant_response = self._send_message(role="user", content=command_output)["content"]
      else:
        print(f'{self.mode} Assistant: {assistant_response}')
        return True
