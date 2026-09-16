from pathlib import Path
from .runtime.environment import Environment
from .runtime.config import Config
from .runtime.registry import Registry
from .memory.manager import MemoryManager
from .models.manager import ModelManager
from .tools.registry import ToolRegistry
from .agents.registry import AgentRegistry
from .core.router import Router
from .evaluation.gates import EvaluationGate
from .learning.ledger import LearningLedger

class Runtime:
    def __init__(self,root,config,env,registry,memory,models,tools,agents,router,evaluator,learning):
        self.root,self.config,self.env=root,config,env; self.registry=registry; self.memory=memory; self.models=models; self.tools=tools; self.agents=agents; self.router=router; self.evaluator=evaluator; self.learning=learning

class Bootstrap:
    def __init__(self,root=None): self.root=Path(root) if root else Path(__file__).resolve().parents[1]
    def start(self,**kwargs):
        env=Environment.detect(); config=Config.load(self.root); registry=Registry(self.root,config)
        memory=MemoryManager(self.root/'storage'/'memory'); models=ModelManager(self.root,config,env)
        tools=ToolRegistry(self.root,env); learning=LearningLedger(self.root/'storage'/'learning')
        agents=AgentRegistry(self.root,models,tools,memory); router=Router(registry,agents,memory)
        evaluator=EvaluationGate()
        return Runtime(self.root,config,env,registry,memory,models,tools,agents,router,evaluator,learning)
