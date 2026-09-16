
from abc import ABC, abstractmethod
class ModelBackend(ABC):
    name="base"
    capabilities=set()
    @abstractmethod
    def generate(self, messages, **kwargs): ...
    def available(self): return True
