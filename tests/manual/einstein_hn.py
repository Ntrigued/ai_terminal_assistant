from assistants.base_assistant import BaseAssistant


astnt = BaseAssistant()
astnt.think_hard = "Einstein"

astnt.query_user("Write a python script to get the articles currently on the front page of Hacker news compiled into a list")
astnt.interaction_loop()
