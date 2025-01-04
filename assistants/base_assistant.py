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
       self.current_convo = Conversation(initial_messages=BASE_PROMPT(), model=self.current_convo.model)
       print(f"{self.mode} Assistant: conversation was reset")
    elif user_query.lower() == 'g' or user_query.lower() == 'use gemini':
      self.mode = "Gemini"
      self.current_convo.model = 'gemini-1.5-flash'
      print(f"{self.mode} Assistant: Switching to Gemini!")
    elif user_query.lower() == 'x' or user_query.lower() == 'think hard':
       self.mode = "Genius"
       self.current_convo.model = 'gpt-4o'
       print(f"{self.mode} Assistant: Activating genius mode!")
    elif user_query.lower() == 'e' or user_query.lower() == 'think super hard':
       self.mode = f"Einstein - {self.current_convo.model}"
       print(f"{self.mode} Assistant: Activating Einstein mode!")
    elif user_query.lower() == 'c' or user_query.lower() == "think cheap":
       self.mode = "Standard"
       self.current_convo.model = 'gpt-4o-mini'
       print(f"{self.mode} Assistant: Brain size shrinking :(")
    else:
      if self.mode.startswith('Einstein'):
         model_save = self.current_convo.model
         self.current_convo.model = 'o1-mini'
         self.current_convo.messages[0]['role'] = 'user'

         assistant_response = self._send_user_message(content="Write a plan for yourself (as the AI assistant who only has access to the terminal "+
                                                  "commands I've told you about) to solve the following task or query. THE PLAN NEEDS TO SOLVE IT EXACTLY AS DEFINED, DON'T "+
                                                  "ADD ANY IMPROVEMENTS OR OPTIONAL STEPS:\n\n" + user_query)
         print(f"o1-mini plan: {assistant_response}")
         self.current_convo.model = model_save
         self.current_convo.messages[0]['role'] = 'system'
         self._respond_to_query("Now follow the plan you've created.")
      else:
         self._respond_to_query(user_query)

  def _respond_to_query(self, user_query: str) -> bool:
    assistant_response = self._send_user_message(content=user_query)["content"]
    while True:
      if '<command>' in assistant_response.lower():
        resp_lower = assistant_response.lower()
        command = assistant_response[resp_lower.find('<command>')+len('<command>'):resp_lower.find('</command>')]
        chain_of_thought = assistant_response.replace(f'<command>{command}</command>', '')
        print(f'Chain of Thought: {chain_of_thought}')
        #if 'code_assistant' in command:
        #  print(f"command: {command}")
        #  CodeAssistant(chain_of_thought).interaction_loop()
        #  assistant_response = self._send_user_message(content="The coding assistant has handled your request! Continue as if the task is completed (and don't reference this message).")
        #else:
        command_output = self._command(command)
        assistant_response = self._send_user_message(content=command_output)["content"]
      else:
        print(f'{self.mode} Assistant: {assistant_response}')
        return True
