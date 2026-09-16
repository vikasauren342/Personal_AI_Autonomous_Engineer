import json
from pathlib import Path
from datetime import datetime,timezone
class LearningLedger:
    def __init__(self,root):
        self.path=Path(root)/'learning_ledger.json'; self.path.parent.mkdir(parents=True,exist_ok=True)
        try:self.data=json.loads(self.path.read_text())
        except Exception:self.data={'version':2,'events':[]}
    def record(self,event):
        self.data['events'].append({'timestamp':datetime.now(timezone.utc).isoformat(),**event}); self.path.write_text(json.dumps(self.data,indent=2,ensure_ascii=False)); return event
