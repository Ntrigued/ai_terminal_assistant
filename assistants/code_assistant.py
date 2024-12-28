from typing import Optional

from openai import OpenAI
import os
import subprocess
import sys
from conversation import Message, Conversation
from prompts import CODE_PROMPT
from .abstract_assistant import AbstractAssistant

class CodeAssistant(AbstractAssistant):
  def __init__(self, task_summary: str):
    super().__init__(starter_prompt=CODE_PROMPT())
    self.task_summary = task_summary

  def interaction_loop(self):
    task_completed = self._respond_to_query(f"task/query: {self.task_summary}")
    while not task_completed:
      task_completed = self.query_user()

  def query_user(self):
    user_query = input("User: ")
    user_query = user_query.strip()
    if user_query.lower() == 'exit assistant':
      sys.exit(0)
    if user_query.lower() == 'exit code_assistant':
      return True
    elif user_query.lower() == 'new convo':
      print('Code Assistant: Cannot start a new conversation while in code mode, send "exit code_assistant" first')
    elif user_query.lower() == 'think hard':
      self.current_convo.model = "gpt-4o"
      print("Code Assistant: Activating genius mode!")
    elif user_query.lower() == "think cheap":
      self.current_convo.model = "gpt-4o-mini"
      print("Code Assistant: Brain size shrinking :(")
    else:
      return self._respond_to_query(user_query)
    return False

  def _respond_to_query(self, user_query: str):
    assistant_response = self._send_message(role="user", content=user_query)["content"]
    while True:
      print(f"Code Assistant: {assistant_response}")
      if '<command>' in assistant_response.lower():
        resp_lower = assistant_response.lower()
        command = assistant_response[resp_lower.find('<command>')+len('<command>'):resp_lower.find('</command>')]
        chain_of_thought = assistant_response.replace(f'<command>{command}</command>', '')
        #print(f'Code Chain of Thought: {chain_of_thought}')
        command_output = self._command(command)
        #print(f'Command Output:\n{command_output}')
        assistant_response = self._send_message(role="user", content=command_output)["content"]
      elif 'exit code_assistant' in assistant_response.lower():
        return True
      else:
        return False
