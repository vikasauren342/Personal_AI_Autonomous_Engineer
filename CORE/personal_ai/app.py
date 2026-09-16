
from .bootstrap import Bootstrap
from .core.orchestrator import Orchestrator

class PersonalAI:
    """Single public entry point. Heavy components are loaded only when needed."""
    def __init__(self, runtime, orchestrator):
        self.runtime = runtime
        self.orchestrator = orchestrator

    @classmethod
    def bootstrap(cls, root=None, **kwargs):
        runtime = Bootstrap(root=root).start(**kwargs)
        return cls(runtime, Orchestrator(runtime))

    def ask(self, query, **kwargs):
        return self.orchestrator.ask(query, **kwargs)

    def health(self):
        return self.orchestrator.health()
