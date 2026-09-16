from pathlib import Path
import os, sys, zipfile, shutil

# Set PERSONAL_AI_PROJECT if your core dataset has a different mounted path.
root_candidates=list(Path('/kaggle/input').rglob('Personal_AI_Autonomous_Development_System_V3'))
zip_candidates=list(Path('/kaggle/input').rglob('*Autonomous*Development*V3*.zip'))
if root_candidates: ROOT=root_candidates[0]
elif zip_candidates:
    ROOT=Path('/kaggle/working/Personal_AI_Autonomous_Development_System_V3')
    if ROOT.exists(): shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True)
    with zipfile.ZipFile(zip_candidates[0]) as z: z.extractall(ROOT)
else: ROOT=Path('/kaggle/working/Personal_AI_Autonomous_Development_System_V3')
sys.path.insert(0,str(ROOT))
# Optional: point this to the extracted writable core copy before launch.
# os.environ['PERSONAL_AI_PROJECT']='/kaggle/working/Personal_AI_AGI_Core_v3_0'
from autonomous_runner.orchestrator import AutonomousRunner
print(AutonomousRunner(ROOT/'autonomous_runner').run_once())
