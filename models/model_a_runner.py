from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

# Load once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer_a = AutoTokenizer.from_pretrained("/Users/somshekharsharma/Qwen/Qwen2.5-0.5B-Instruct", local_files_only=True)
model_a = AutoModelForCausalLM.from_pretrained("/Users/somshekharsharma/Qwen/Qwen2.5-0.5B-Instruct", local_files_only=True).to(device)

def chat_with_model_a(prompt):
    input_ids = tokenizer_a(prompt, return_tensors="pt").input_ids.to(model_a.device)
    output = model_a.generate(input_ids, max_new_tokens=256, do_sample=True, temperature=0.7)
    decoded = tokenizer_a.decode(output[0], skip_special_tokens=True).strip()

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

    return assistant_response, dialogue_update, obs