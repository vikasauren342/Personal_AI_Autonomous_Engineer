
from pathlib import Path

PROTECTED = [
    "Personal_AI_AGI_Core_v3_0/personal_ai",
]

DANGEROUS_WORDS = [
    "rm -rf", "mkfs", "shutdown", "reboot",
    "curl | sh", "wget | sh", "password", "private key",
    "api_key", "secret", "token"
]

def path_is_protected(path, project_root):
    p = Path(path).resolve()
    root = Path(project_root).resolve()
    try:
        rel = p.relative_to(root)
    except ValueError:
        return False
    s = str(rel).replace("\\", "/")
    return any(s == x or s.startswith(x + "/") for x in ["personal_ai"])

def command_requires_stop(command):
    c = command.lower()
    return any(x in c for x in DANGEROUS_WORDS)

def require_manual(reason, root):
    p = Path(root) / "state" / "MANUAL_INTERVENTION_REQUIRED.json"
    p.write_text(
        __import__("json").dumps({"manual_intervention_required": True, "reason": reason}, indent=2),
        encoding="utf-8"
    )
    return p
