import sys, pathlib, json
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personal_ai.app import PersonalAI

ai=PersonalAI.bootstrap(ROOT)
print(json.dumps(ai.health(),indent=2,default=str))
print('\n=== SMOKE TEST ===')
print(json.dumps(ai.ask('Explain the architecture of my Personal AI.'),indent=2,ensure_ascii=False,default=str))
