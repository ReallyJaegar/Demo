import gradio as gr
from utils.dialogue_history import DialogueHistory
from utils.tool_registry import get_tools_for_domain
from utils.system_prompts import givesysprompt
 
# Placeholder runners
from models.model_a_runner import chat_with_model_a
from models.model_b_runner import chat_with_model_b
 
dialogue_a = DialogueHistory()
dialogue_b = DialogueHistory()
 
domains = ["finance", "medical"]
 
def on_select_domain(index,domain=None):
    tool_str = get_tools_for_domain(index)
    return tool_str
 
def chat(index, user_input, history_a, history_b):
    tools = get_tools_for_domain(index)
 
    full_prompt_a = f"{tools}\n{dialogue_a.get()}\n<user>{user_input}</user>"
    full_prompt_b = f"{tools}\n{dialogue_b.get()}\n<user>{user_input}</user>"
 
    response_a, tool_a, obs_a = chat_with_model_a(full_prompt_a)
    response_b, tool_b, obs_b = chat_with_model_b(full_prompt_b)
 
    dialogue_a.append(user_input, response_a, tool_a, obs_a)
    dialogue_b.append(user_input, response_b, tool_b, obs_b)
 
    return response_a, response_b, dialogue_a.get(), dialogue_b.get()
with gr.Blocks() as app:
    # domain = gr.Dropdown(choices=domains, label="Select Domain")
    index = gr.Number(label="Enter a number (0 to 3999)", minimum=0, maximum=3999)
    tool_output = gr.Textbox(label="Available Tools", interactive=False)
 
    index.change(fn=on_select_domain, inputs=index, outputs=tool_output)
 
    with gr.Row():
        chatbot_a = gr.Chatbot(label="LLM A (RL Finetuned)")
        chatbot_b = gr.Chatbot(label="LLM B (Non-RL)")
 
    user_input = gr.Textbox(label="Your Message")
    submit_btn = gr.Button("Send")
 
    # Hidden fields for tracking dialogue history
    history_a = gr.State("")
    history_b = gr.State("")
 
    def chat(index, user_input, hist_a, hist_b):
 
        dialogue_a = DialogueHistory()
        dialogue_a.history = hist_a
 
        dialogue_b = DialogueHistory()
        dialogue_b.history = hist_b
 
        
        sys=givesysprompt(index)
 
       
        full_prompt_a = f"{dialogue_a.get()}\n<user>{user_input}</user>"
        full_prompt_b = f"{dialogue_b.get()}\n<user>{user_input}</user>"
 
        _chat_a = [
            {"role": "system", "content": sys},
            {"role": "user", "content":full_prompt_a }
        ]
 
        _chat_b = [
            {"role": "system", "content": sys},
            {"role": "user", "content":full_prompt_b }
        ]
 
 
        response_a, tool_a, obs_a = chat_with_model_a(_chat_a)
        response_b, tool_b, obs_b = chat_with_model_b(_chat_b)
        # print(response_a)
 
        dialogue_a.append(user_input, response_a, tool_a, obs_a)
        dialogue_b.append(user_input, response_b, tool_b, obs_b)
        # print(dialogue_a)
        # print(user_input)
        # print(tool_a)
        print(type(response_a))
        
        think_a = "Think: "+response_a.split("<think>")[-1].split("</think>")[0].strip().replace("\n","")
 
        temp_a = "\nResponse: "+response_a.split("<response>")[-1].split("</response>")[0].strip().replace("\n","")
 
 
        if "<response>" in response_a:
            think_a+=temp_a
 
        temp_a= "\nTool: "+response_a.split("<tool_call>")[-1].split("</tool_call>")[0].strip().replace("\n","")
 
        if "<tool_call>" in response_a:
            think_a+=temp_a
 
        
        think_b = "Think: "+response_b.split("<think>")[-1].split("</think>")[0].strip().replace("\n","")
 
        temp_b = "\nResponse: "+response_b.split("<response>")[-1].split("</response>")[0].strip().replace("\n","")
 
        if "<response>" in response_b:
            think_b+=temp_b
 
        temp_b = "\nTool: "+response_b.split("<tool_call>")[-1].split("</tool_call>")[0].strip().replace("\n","")
 
        if "<tool_call>" in response_b:
            think_b+=temp_b
        
        # response_a = response_a.split("<think>")[-1].split("</think>")[0].strip().replace("\n","")
        # response_b = response_b.split("<response>")[-1].split("</response>")[0].strip().replace("\n","")
        print("response a is :", response_a)
        print("response b is :", response_b)
 
        # response_a="temp"
        return [(user_input, str(think_a).strip())], [(user_input, think_b)], dialogue_a.history, dialogue_b.history
 
    submit_btn.click(fn=chat,
                     inputs=[index, user_input, history_a, history_b],
                     outputs=[chatbot_a, chatbot_b, history_a, history_b])
 
app.launch()
