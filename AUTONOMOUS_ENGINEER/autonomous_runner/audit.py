import hashlib, json, subprocess, sys
from pathlib import Path

FOUNDATION = {
 "personal_ai/bootstrap.py":"a36671eef8371dc1ffb7b790d977cfd2cb4419a489cdb442613ebc3fe1f0a5db",
 "personal_ai/core/contracts.py":"7922dae35487a6f8d0d1e2c4d5fa2e4512e780a2cbebb9c25cd0624e89b69080",
 "personal_ai/core/planner.py":"112015d303fad1a2ec44617b2f03ba61dcf63f9ce779dd209ac22dfd1864497a",
 "personal_ai/execution/engine.py":"36f847ca5972e034a44659ea932727379edaddcde735ef54de52ed1a305cf56a",
}

def sha(p):
 h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()

def audit(project):
 project=Path(project).resolve(); out={"project":str(project),"foundation":{},"tests":{},"status":"UNKNOWN"}
 if not project.exists(): out["status"]="MISSING"; return out
 for rel,want in FOUNDATION.items():
  p=project/rel
  out["foundation"][rel]={"exists":p.exists(),"sha256":sha(p) if p.exists() else None,"protected_match":p.exists() and sha(p)==want}
 try:
  r=subprocess.run([sys.executable,"-m","pytest","-q"],cwd=project,text=True,capture_output=True,timeout=900)
  out["tests"]={"returncode":r.returncode,"passed":r.returncode==0,"stdout":r.stdout[-8000:],"stderr":r.stderr[-8000:]}
 except Exception as e: out["tests"]={"passed":False,"error":repr(e)}
 out["status"]="PASS" if all(x["protected_match"] for x in out["foundation"].values()) and out["tests"].get("passed") else "REPAIR_REQUIRED"
 return out
