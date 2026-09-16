
import json
from pathlib import Path
class Config:
    @staticmethod
    def load(root):
        p=Path(root)/"config"/"system.json"
        data=json.loads(p.read_text()) if p.exists() else {}
        return data
