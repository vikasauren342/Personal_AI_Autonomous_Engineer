from pathlib import Path
from .base import ModelBackend


class QwenBackend(ModelBackend):
    """Lazy local Transformers backend for Qwen-family causal LMs.

    The model is intentionally external to this package. A complete local model
    directory is required; tokenizer-only assets are not treated as loadable.
    """

    name = "qwen_local"
    capabilities = {"chat", "reasoning", "json", "planning"}

    def __init__(self, model_path):
        self.model_path = Path(model_path)
        self._model = None
        self._tokenizer = None

    def available(self):
        if not (self.model_path / "config.json").exists():
            return False
        if not any((self.model_path / n).exists() for n in ("tokenizer.json", "tokenizer_config.json")):
            return False
        # Do not mistake tokenizer/config-only bundles for complete model weights.
        weight_patterns = ("*.safetensors", "*.bin", "*.gguf")
        return any(self.model_path.glob(p) for p in weight_patterns)

    def _load(self):
        if self._model is not None:
            return
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_path, local_files_only=True
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map="auto",
            torch_dtype="auto",
            local_files_only=True,
        )

    def generate(self, messages, **kwargs):
        self._load()
        text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer(text, return_tensors="pt").to(self._model.device)
        generation_kwargs = {
            "max_new_tokens": int(kwargs.get("max_new_tokens", 512)),
            "do_sample": bool(kwargs.get("do_sample", False)),
        }
        if kwargs.get("temperature") is not None:
            generation_kwargs["temperature"] = float(kwargs["temperature"])
        if kwargs.get("top_p") is not None:
            generation_kwargs["top_p"] = float(kwargs["top_p"])
        out = self._model.generate(**inputs, **generation_kwargs)
        return self._tokenizer.decode(
            out[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        )
