
from .base import ModelBackend
class FallbackBackend(ModelBackend):
    name="fallback"
    capabilities={"chat","routing","planning"}
    def generate(self, messages, **kwargs):
        user = messages[-1]["content"] if messages else ""
        return ("Local model unavailable. I can still route, validate, store memory, "
                "and execute deterministic tools. Attach a compatible local model "
                "or enable a future model backend. Request: " + user)
