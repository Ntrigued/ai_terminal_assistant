from assistant import Assistant

astnt = Assistant()
print(astnt._command("pwd"))
astnt._send_message("user", "reply with: hello")
