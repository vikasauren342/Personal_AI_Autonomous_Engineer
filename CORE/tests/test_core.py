import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personal_ai.app import PersonalAI
def test_boot():
    ai=PersonalAI.bootstrap(ROOT); h=ai.health(); assert 'general' in h['agents']; assert 'fallback' in h['models']
def test_routes():
    ai=PersonalAI.bootstrap(ROOT); assert ai.runtime.router.route('write python code')=='coding'; assert ai.runtime.router.route('research this')=='research'
