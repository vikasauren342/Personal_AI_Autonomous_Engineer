
import subprocess, sys
from pathlib import Path
from .safety import command_requires_stop

def execute_python_file(path, cwd, timeout=900):
    path = Path(path)
    if not path.exists():
        return {"passed": False, "reason": "file missing"}
    r = subprocess.run(
        [sys.executable, str(path)],
        cwd=cwd, text=True, capture_output=True, timeout=timeout
    )
    return {
        "passed": r.returncode == 0,
        "returncode": r.returncode,
        "stdout": r.stdout[-12000:],
        "stderr": r.stderr[-12000:]
    }

def execute_command(command, cwd, timeout=900):
    if command_requires_stop(command):
        return {"passed": False, "manual_stop": True, "reason": "unsafe command"}
    r = subprocess.run(command, cwd=cwd, shell=True, text=True,
                       capture_output=True, timeout=timeout)
    return {
        "passed": r.returncode == 0,
        "returncode": r.returncode,
        "stdout": r.stdout[-12000:],
        "stderr": r.stderr[-12000:]
    }
