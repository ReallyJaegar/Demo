import gradio as gr
from utils.dialogue_history import DialogueHistory
from utils.tool_registry import get_tools_for_domain

# Placeholder runners
from models.model_a_runner import chat_with_model_a
from models.model_b_runner import chat_with_model_b

dialogue_a = DialogueHistory()
dialogue_b = DialogueHistory()

domains = ["finance", "medical"]

def on_select_domain(domain):
    tool_str = get_tools_for_domain(domain)
    return tool_str

def chat(domain, user_input, history_a, history_b):
    tools = get_tools_for_domain(domain)

    full_prompt_a = f"{tools}\n{dialogue_a.get()}\n<user>{user_input}</user>"
    full_prompt_b = f"{tools}\n{dialogue_b.get()}\n<user>{user_input}</user>"

    response_a, tool_a, obs_a = chat_with_model_a(full_prompt_a)
    response_b, tool_b, obs_b = chat_with_model_b(full_prompt_b)

    dialogue_a.append(user_input, response_a, tool_a, obs_a)
    dialogue_b.append(user_input, response_b, tool_b, obs_b)

    return response_a, response_b, dialogue_a.get(), dialogue_b.get()
with gr.Blocks() as app:
    domain = gr.Dropdown(choices=domains, label="Select Domain")
    tool_output = gr.Textbox(label="Available Tools", interactive=False)

    domain.change(fn=on_select_domain, inputs=domain, outputs=tool_output)

    with gr.Row():
        chatbot_a = gr.Chatbot(label="LLM A (RL Finetuned)")
        chatbot_b = gr.Chatbot(label="LLM B (Non-RL)")

    user_input = gr.Textbox(label="Your Message")
    submit_btn = gr.Button("Send")

    # Hidden fields for tracking dialogue history
    history_a = gr.State("")
    history_b = gr.State("")

    def chat(domain, user_input, hist_a, hist_b):
        tools = get_tools_for_domain(domain)

        dialogue_a = DialogueHistory()
        dialogue_a.history = hist_a

        dialogue_b = DialogueHistory()
        dialogue_b.history = hist_b

        full_prompt_a = f"{tools}\n{dialogue_a.get()}\n<user>{user_input}</user>"
        full_prompt_b = f"{tools}\n{dialogue_b.get()}\n<user>{user_input}</user>"

        response_a, tool_a, obs_a = chat_with_model_a(full_prompt_a)
        response_b, tool_b, obs_b = chat_with_model_b(full_prompt_b)

        dialogue_a.append(user_input, response_a, tool_a, obs_a)
        dialogue_b.append(user_input, response_b, tool_b, obs_b)

        return [(user_input, response_a)], [(user_input, response_b)], dialogue_a.history, dialogue_b.history

    submit_btn.click(fn=chat,
                     inputs=[domain, user_input, history_a, history_b],
                     outputs=[chatbot_a, chatbot_b, history_a, history_b])

app.launch()