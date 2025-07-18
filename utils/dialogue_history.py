class DialogueHistory:
    def __init__(self):
        self.history = ""
 
    def append(self, user_msg, assistant_msg, tool_call="", obs=""):
        self.history += f"<user>{user_msg}</user><response>{assistant_msg}</response>"
        if tool_call:
            self.history += f"<tool_call>{tool_call}</tool_call>"
        if obs:
            self.history += f"<obs>{obs}</obs>"
 
    def get(self):
        return f"**Dialogue History Starts**\n{self.history}\n**Dialogue History Ends**"
 
    def reset(self):
        self.history = ""
