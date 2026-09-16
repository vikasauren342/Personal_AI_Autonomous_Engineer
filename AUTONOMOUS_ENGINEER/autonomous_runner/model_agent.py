
import json, os, re, sys
from pathlib import Path

def find_model():
    candidates = [
        os.environ.get("PERSONAL_AI_MODEL_DIR"),
        "/kaggle/working/personal_ai_models/qwen2.5-1.5b-instruct",
        "/kaggle/input/personal-ai-qwen",
    ]
    for p in candidates:
        if p and Path(p).exists() and (Path(p)/"config.json").exists():
            return Path(p)
    return None

def local_qwen(messages, model_dir=None, max_new_tokens=512):
    model_dir = model_dir or find_model()
    if model_dir is None:
        raise RuntimeError("No local Qwen checkpoint found.")

    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tok = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, device_map="auto", torch_dtype="auto", local_files_only=True
    )
    inputs = tok.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True,
        enable_thinking=False, return_tensors="pt"
    )
    device = next(model.parameters()).device
    inputs = inputs.to(device)
    with torch.inference_mode():
        out = model.generate(
            inputs, max_new_tokens=max_new_tokens,
            do_sample=False, pad_token_id=tok.eos_token_id
        )
    return tok.decode(out[0][inputs.shape[-1]:], skip_special_tokens=True).strip()

def extract_json(text):
    start = text.find("{")
    if start < 0:
        raise ValueError("No JSON object in model output")
    depth, quoted, esc = 0, False, False
    for i in range(start, len(text)):
        ch = text[i]
        if esc:
            esc = False; continue
        if ch == "\\":
            esc = True; continue
        if ch == '"':
            quoted = not quoted; continue
        if not quoted:
            if ch == "{": depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i+1])
    raise ValueError("Incomplete JSON object")
