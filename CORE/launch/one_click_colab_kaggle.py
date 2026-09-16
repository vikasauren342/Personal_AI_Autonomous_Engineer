# Copy/paste this whole cell in Colab/Kaggle after the project folder is available.
import os,sys,pathlib
ROOT=pathlib.Path(os.environ.get('PERSONAL_AI_ROOT','/content/Personal_AI_AGI_Ready_Core_v3_0'))
sys.path.insert(0,str(ROOT))
from personal_ai.app import PersonalAI
ai=PersonalAI.bootstrap(ROOT)
print(ai.health())
print(ai.ask('Run a system smoke test and summarize the result.'))
