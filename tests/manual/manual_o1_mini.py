from assistants.base_assistant import BaseAssistant

from time import sleep


astnt = BaseAssistant()
astnt.current_convo.model = 'o1-mini'
astnt.current_convo.messages[0]['role'] = 'user'

assistant_response = astnt._send_message(role="user", content="Write a plan for yourself (as the AI assistant who only has access to the terminal "+
"commands I've told you about) to solve the following task or query. SOLVE IT EXACTLY AS DEFINED, DON'T ADD ANY IMPROVEMENTS OR OPTIONAL STEPS:\n\n"+
"Determine how to get the articles on the front page of Hacker News, verify this by going through the steps manually, and then write a script to do so.")
print(f"Assistant: {assistant_response}")
sleep(10)
astnt.current_convo.model = "gpt-4o-mini"
astnt.current_convo.messages[0]['role'] = 'system'
astnt._respond_to_query("Now follow the plan you've created.")
