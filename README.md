**work-in-progress**

# AI Terminal Assistant

A little project where I try to create an AI assistant that runs in the terminal and can gather info / perform actions on my behalf by executing shell commands.

Currently, only uses OpenAI models: GPT-4o, GPT-4o-mini, o1-mini. Gemini-1.5-flash was **just** also added but is basically unusable.
The script will start in "Standard Mode", which uses the <code>gpt-4o-mini</code> model.

### Prompt Commands:
**Enter these at the user prompt to run the commands**
* **exit assistant**: Exit the program
* **new convo**: Erase all conversation history, starting over with just the initial prompt messages that all conversations start with
* **use gemini** or **g**: Switch to the <code>gemini-1.5.-flash</code> model
* **think cheap** or **c**: Switch to the <code>gpt-4o-mini</code> model
* **think hard** or **x**: Switch to the <code>gpt-4o</code> model
* **think super hard** or **e**: Switch to the following: each user message is first passed to the <code>o1-mini</code> model with a special prompt (telling it to create a plan to fulfill the request). This <code>o1-mini</code> message is then passed to the previously selected model with a special prompt telling it to follow the given plan.


## Conversation Example 
(command output removed, it would normally be shown in the conversation. The assistant wrote these responses in markdown.)
```
Standard Assistant: What can I help you with?
User: Make a list of all methods in assistants/abstract_assistant.py, with a 1-2 sentence summary of what each does
Chain of Thought: I will first extract the content of `assistants/abstract_assistant.py`, and then I will analyze the code to identify and summarize the methods.


Running command: cat assistants/abstract_assistant.py
Command output: <removed>
Standard Assistant: Here is a list of the methods in the `assistants/abstract_assistant.py` file along with a brief summary of what each does:

1. **`__init__(self, starter_prompt, model="gpt-4o-mini")`**:
   - Initializes an instance of `AbstractAssistant`, setting up the OpenAI client using an API key and establishing a new conversation with an initial prompt.

2. **`_command(self, command) -> str`**:
   - Executes a shell command while ensuring the user's permission for potentially destructive commands (like `mv` or `rm`). It captures the output of the command and returns it as a string, limiting execution time to 60 seconds.

3. **`_send_message(self, role, content) -> Message`**:
   - Sends a message to the OpenAI chat completion model and manages the conversation history. It adds user messages and the assistant's responses to the conversation, while handling any errors during the interaction.

If you need further details or have more questions, feel free to ask!
User: What models does base_assistant.py use?
Chain of Thought: I will check the content of `assistants/base_assistant.py` to identify which models are being used in that file.


Running command: cat assistants/base_assistant.py
Command output: <removed>
Standard Assistant: The `assistants/base_assistant.py` file uses the following models:

1. **`gpt-4o-mini`**:
   - This is the default model used when the conversation is initialized or reset.

2. **`o1-mini`**:
   - This model is set when the assistant is in "Genius" or "Einstein" mode and is used to generate a plan for solving the user's query.

3. **`gpt-4o`**:
   - This model is selected when the assistant is in "Einstein" mode after a plan has been generated using the `o1-mini` model.

The assistant dynamically switches between these models based on user interactions and the chosen mode of operation. If you have any further questions or need additional details, feel free to ask!
User:
```
