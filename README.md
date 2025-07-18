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
│  ├─ __pycache__
│  │  ├─ model_a_runner.cpython-312.pyc
│  │  ├─ model_a_runner.cpython-313.pyc
│  │  └─ model_b_runner.cpython-313.pyc
│  ├─ model_a_runner.py
│  └─ model_b_runner.py
├─ prompts
│  └─ system_promts.json
├─ toolextract.py
└─ utils
   ├─ .py
   ├─ __pycache__
   │  ├─ dialogue_history.cpython-312.pyc
   │  ├─ dialogue_history.cpython-313.pyc
   │  ├─ tool_registry.cpython-312.pyc
   │  └─ tool_registry.cpython-313.pyc
   ├─ dialogue_history.py
   ├─ system_prompts.py
   └─ tool_registry.py
```