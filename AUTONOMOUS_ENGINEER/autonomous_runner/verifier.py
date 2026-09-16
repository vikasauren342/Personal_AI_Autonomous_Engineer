
import json, subprocess, sys
from pathlib import Path

def run_tests(project):
    project = Path(project)
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=project, text=True, capture_output=True, timeout=900
    )
    return {
        "passed": r.returncode == 0,
        "returncode": r.returncode,
        "stdout": r.stdout[-12000:],
        "stderr": r.stderr[-12000:]
    }

def smoke(project):
    project = Path(project)
    launcher = project / "launch" / "run.py"
    if not launcher.exists():
        return {"passed": False, "reason": "launch/run.py missing"}
    r = subprocess.run(
        [sys.executable, str(launcher)],
        cwd=project, text=True, capture_output=True, timeout=900
    )
    return {
        "passed": r.returncode == 0,
        "returncode": r.returncode,
        "stdout": r.stdout[-12000:],
        "stderr": r.stderr[-12000:]
    }

def verify(project):
    tests = run_tests(project)
    smoke_result = smoke(project)
    return {
        "passed": tests["passed"] and smoke_result["passed"],
        "tests": tests,
        "smoke": smoke_result
    }
