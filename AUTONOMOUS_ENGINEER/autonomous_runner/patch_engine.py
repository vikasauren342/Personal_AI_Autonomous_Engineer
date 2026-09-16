"""Bounded implementation engine.
Applies only unified-diff patches inside the configured project root, refuses protected foundation paths,
and always creates a pre-change snapshot before applying a patch.
"""
from pathlib import Path
import re, shutil, subprocess, time

PROTECTED = {
    "personal_ai/bootstrap.py",
    "personal_ai/core/contracts.py",
    "personal_ai/core/planner.py",
    "personal_ai/execution/engine.py",
}

def _changed_paths(diff_text):
    return [p for p in re.findall(r'^\+\+\+ b/(.+)$', diff_text, flags=re.M) if p != '/dev/null']

def validate_patch(diff_text, project):
    project = Path(project).resolve()
    paths = _changed_paths(diff_text)
    if not paths:
        return {"allowed": False, "reason": "patch contains no changed files"}
    for rel in paths:
        rel = rel.replace('\\','/')
        if rel in PROTECTED:
            return {"allowed": False, "reason": f"protected foundation file: {rel}"}
        if rel.startswith("../") or rel.startswith("/"):
            return {"allowed": False, "reason": f"path escapes project: {rel}"}
    return {"allowed": True, "paths": paths}

def apply_patch(diff_text, project, patch_id="patch"):
    project = Path(project).resolve()
    check = validate_patch(diff_text, project)
    if not check["allowed"]:
        return check
    backup = project.parent / f".autonomous_backup_{patch_id}_{int(time.time())}"
    shutil.copytree(project, backup)
    patch_file = project.parent / f".{patch_id}.diff"
    patch_file.write_text(diff_text, encoding="utf-8")
    try:
        r = subprocess.run(["git", "apply", "--check", str(patch_file)], cwd=project, text=True, capture_output=True, timeout=120)
        if r.returncode != 0:
            return {"allowed": True, "applied": False, "reason": "git apply --check failed", "stderr": r.stderr[-8000:], "backup": str(backup)}
        r = subprocess.run(["git", "apply", str(patch_file)], cwd=project, text=True, capture_output=True, timeout=120)
        return {"allowed": True, "applied": r.returncode == 0, "stdout": r.stdout[-8000:], "stderr": r.stderr[-8000:], "backup": str(backup), "paths": check["paths"]}
    finally:
        patch_file.unlink(missing_ok=True)
