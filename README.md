# Multi-Turn LLM Comparison App

Gradio applications to qualitatively evaluate multi turn tool capability of RL-finetuned LLM with vanilla LLM.


## Project Structure
```
📦 Demo
├─ app.py
├─ domains
│  ├─ __init.py__
│  └─ finance.py
├─ models
│  ├─ model_a_runner.py
│  └─ model_b_runner.py
├─ prompts
│  └─ system_promts.json
├─ toolextract.py
└─ utils
   ├─ dialogue_history.py
   ├─ system_prompts.py
   └─ tool_registry.py
```