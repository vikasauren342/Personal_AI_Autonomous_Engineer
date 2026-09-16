import os
from pathlib import Path
from .fallback import FallbackBackend
from .qwen import QwenBackend


class ModelManager:
    """Model registry with explicit external-model discovery and safe fallback."""

    def __init__(self, root, config, env):
        self.root = Path(root)
        self.config = config
        self.env = env
        self.backends = {}
        self._register()

    def _candidate_paths(self):
        env_path = os.environ.get("PERSONAL_AI_MODEL_DIR")
        if env_path:
            yield Path(env_path)

        # Common project-local locations.
        for p in (
            self.root / "models" / "qwen3-8b-awq",
            self.root / "models" / "qwen3-8b",
            self.root / "models" / "qwen2.5-1.5b-instruct",
            self.root / "models" / "qwen",
        ):
            yield p

        # Common Kaggle/Colab dataset layouts. They are only candidates;
        # availability() still requires actual model weights.
        for p in (
            Path("/kaggle/input/qwen3-8b-awq"),
            Path("/kaggle/input/qwen3-8b"),
            Path("/kaggle/input/personal-ai-qwen"),
            Path("/kaggle/input/datasets/vikaschandoliya/personal-ai-qwen"),
            Path("/content/qwen3-8b-awq"),
            Path("/content/personal_ai/models/qwen2.5-1.5b-instruct"),
        ):
            yield p

    def _register(self):
        for path in self._candidate_paths():
            backend = QwenBackend(path)
            if backend.available():
                self.backends[backend.name] = backend
                break
        self.backends["fallback"] = FallbackBackend()

    def choose(self, capability="chat"):
        for backend in self.backends.values():
            if capability in backend.capabilities and backend.available():
                return backend
        return self.backends["fallback"]

    def generate(self, messages, capability="chat", **kwargs):
        return self.choose(capability).generate(messages, **kwargs)
