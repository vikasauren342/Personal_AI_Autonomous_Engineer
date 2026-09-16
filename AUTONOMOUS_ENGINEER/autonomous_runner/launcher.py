
from pathlib import Path
import sys, json, os

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent

if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from autonomous_runner.orchestrator import AutonomousRunner

print("="*78)
print("PERSONAL AI — AUTONOMOUS DEVELOPMENT RUNNER")
print("="*78)
print("Runner:", ROOT)
print("Project:", (PARENT/"Personal_AI_AGI_Core_v3_0").resolve())
print("")

runner = AutonomousRunner(ROOT)
result = runner.run_once()

print("\n=== RUNNER RESULT ===")
print(json.dumps(result, indent=2, ensure_ascii=False))
print("\nState:", ROOT/"state"/"current_state.json")
print("Reports:", ROOT/"reports")
print("Checkpoints:", ROOT/"checkpoints")
print("Logs:", ROOT/"logs")
print("="*78)
