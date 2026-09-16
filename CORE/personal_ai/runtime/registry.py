
import json
from pathlib import Path
class Registry:
    def __init__(self, root, config):
        self.root=Path(root); self.config=config
        self.models=self._load("config/models.json")
        self.agents=self._load("config/agents.json")
        self.tools=self._load("config/tools.json")
    def _load(self, rel):
        p=self.root/rel
        return json.loads(p.read_text()) if p.exists() else {}
