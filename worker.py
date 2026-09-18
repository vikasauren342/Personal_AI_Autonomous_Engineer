import os
from threading import Lock

import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_PATH = os.environ.get("PERSONAL_AI_MODEL_DIR")
WORKER_NAME = os.environ.get("WORKER_NAME", "gpu-worker")
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen2.5-3B-Instruct")

if not MODEL_PATH:
    raise RuntimeError(
        "PERSONAL_AI_MODEL_DIR environment variable is required"
    )


app = FastAPI(
    title="Personal AI GPU Worker",
    version="1.1.0",
)


_tokenizer = None
_model = None
_model_lock = Lock()


class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 256


def load_model():
    global _tokenizer, _model

    if _model is not None:
        return

    with _model_lock:
        if _model is not None:
            return

        if not torch.cuda.is_available():
            raise RuntimeError("CUDA GPU is not available")

        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_PATH,
            local_files_only=True,
        )

        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float16,
            local_files_only=True,
        ).to("cuda")


@app.get("/worker/health")
def health():
    return {
        "status": "ok",
        "worker": WORKER_NAME,
        "cuda": torch.cuda.is_available(),
        "gpu": (
            torch.cuda.get_device_name(0)
            if torch.cuda.is_available()
            else None
        ),
        "model": MODEL_NAME,
        "model_loaded": _model is not None,
    }


@app.post("/worker/generate")
def generate(request: GenerateRequest):
    load_model()

    messages = [
        {
            "role": "user",
            "content": request.prompt,
        }
    ]

    text = _tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = _tokenizer(
        text,
        return_tensors="pt",
    ).to("cuda")

    with torch.no_grad():
        output = _model.generate(
            **inputs,
            max_new_tokens=request.max_new_tokens,
            do_sample=False,
        )

    answer = _tokenizer.decode(
        output[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )

    return {
        "answer": answer,
        "model": MODEL_NAME,
        "worker": WORKER_NAME,
    }