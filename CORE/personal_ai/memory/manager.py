
import json, uuid
from datetime import datetime, timezone
from pathlib import Path
class MemoryManager:
    def __init__(self, root):
        self.root=Path(root); self.root.mkdir(parents=True, exist_ok=True)
        self.path=self.root/"memory.json"
        self.data={"version":2,"items":[]}
        if self.path.exists():
            try:self.data=json.loads(self.path.read_text())
            except Exception:pass
    def add(self, content, category="episodic", source="system", confidence=1.0, metadata=None):
        item={"id":str(uuid.uuid4()),"category":category,"content":content,
              "source":source,"confidence":confidence,"metadata":metadata or {},
              "created_at":datetime.now(timezone.utc).isoformat()}
        self.data["items"].append(item); self.save(); return item
    def search(self, query, limit=8):
        terms=set(query.lower().split())
        scored=[]
        for x in self.data.get("items",[]):
            text=str(x.get("content","")).lower()
            score=sum(t in text for t in terms)
            if score: scored.append((score,x))
        scored.sort(key=lambda z:z[0], reverse=True)
        return [x for _,x in scored[:limit]]
    def save(self): self.path.write_text(json.dumps(self.data,indent=2,ensure_ascii=False))
