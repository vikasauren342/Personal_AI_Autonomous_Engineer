
import json, re
from pathlib import Path

def inspect_project(project):
    project = Path(project)
    files = [p for p in project.rglob("*") if p.is_file()]
    return {
        "file_count": len(files),
        "python_files": len([p for p in files if p.suffix == ".py"]),
        "has_tests": (project / "tests").exists(),
        "has_personal_ai": (project / "personal_ai").exists(),
        "has_launch": (project / "launch").exists(),
    }

def discover_current_notebook(notebook):
    if not notebook.exists():
        return {}
    data = json.loads(notebook.read_text(encoding="utf-8"))
    milestones = []
    for cell in data.get("cells", []):
        src = "".join(cell.get("source", []))
        for m in re.findall(r"KAGGLE-\d{3}(?:-[A-Z0-9]+)*", src):
            milestones.append(m)
    return {"milestones_seen": list(dict.fromkeys(milestones))}

def next_milestone(state, notebook_info):
    history = state.get("history", [])
    done = set(x.get("milestone") for x in history if x.get("event") == "PASS")
    seen = notebook_info.get("milestones_seen", [])
    for m in seen:
        if m not in done:
            return m
    # After the historical notebook, let the model define the next engineering milestone.
    last = state.get("last_successful_milestone") or (seen[-1] if seen else "UNKNOWN")
    return f"AUTO-NEXT-AFTER-{last}"
