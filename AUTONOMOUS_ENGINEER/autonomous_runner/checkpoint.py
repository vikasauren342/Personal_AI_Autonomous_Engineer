
import json, time
from pathlib import Path

class Checkpoint:
    def __init__(self, root):
        self.root = Path(root)
        self.state_dir = self.root / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.state_dir / "current_state.json"

    def load(self):
        if not self.path.exists():
            return {
                "status": "NEW",
                "current_milestone": None,
                "last_successful_milestone": None,
                "attempts": 0,
                "repairs": 0,
                "history": []
            }
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, state):
        state["updated_at"] = time.time()
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)

    def event(self, state, event, **data):
        state.setdefault("history", []).append({
            "time": time.time(), "event": event, **data
        })
        self.save(state)
