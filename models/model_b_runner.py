from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
 
# Load once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer_b = AutoTokenizer.from_pretrained("/storage/som/ToolRL/checkpoints/TinyZero/grpo-qwen2.5-3b/actor/global_step_2550", local_files_only=True)
model_b = AutoModelForCausalLM.from_pretrained("/storage/som/ToolRL/checkpoints/TinyZero/grpo-qwen2.5-3b/actor/global_step_2550", local_files_only=True).to(device)
 
def chat_with_model_a(messages):
 
    tokenized_chat = tokenizer_b.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, return_tensors="pt")
    # prompt=tokenizer_a.decode(tokenized_chat[0])
    input_ids = tokenizer_b(tokenized_chat, return_tensors="pt").input_ids.to(model_b.device)
    output = model_b.generate(input_ids, max_new_tokens=256, do_sample=True, temperature=0.7)
    decoded = tokenizer_b.decode(output[0], skip_special_tokens=False).strip()
    decoded=decoded.split("<|im_start|>assistant")[-1].split("<|im_end|>")[0].strip()
 
    # Extract tool_call if present
    tool_call_match = re.search(r"<tool_call>(.*?)</tool_call>", decoded, re.DOTALL)
 
    if tool_call_match:
        # If tool_call is present, extract and return separately
        tool_call = f"<tool_call>{tool_call_match.group(1).strip()}</tool_call>"
        assistant_response = decoded  # full raw model reply
        dialogue_update = tool_call
        obs = "<obs>None</obs>"  # Update this if you implement tool execution later
    else:
        # If it's a normal response
        assistant_response = decoded
        dialogue_update = f"<response>{assistant_response}</response>"
        obs = "<obs>None</obs>"
    print(decoded)
 
    return assistant_response, dialogue_update, obs
