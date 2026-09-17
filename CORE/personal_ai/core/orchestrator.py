import uuid
from .contracts import Task
from .planner import Planner
from personal_ai.execution.engine import ExecutionEngine

class Orchestrator:
    def __init__(self,runtime):
        self.runtime=runtime; self.planner=Planner(runtime.models)
        self.engine=ExecutionEngine(runtime.tools,runtime.evaluator,runtime.learning,runtime.config.get('execution',{}).get('max_autonomous_steps',5))
    def ask(self,query,autonomous=False,**kwargs):
        route=self.runtime.router.route(query); memories=self.runtime.memory.search(query)
        context={'route':route,'memories':memories}
        result=self.runtime.agents.get(route).run(query,context=context)
        self.runtime.memory.add(query,category='episodic',source='user')
        self.runtime.memory.add(result,category='interaction',source='agent',metadata={'route':route})
        if autonomous:
            task=Task(str(uuid.uuid4()),query,{'route':route})
            execution=self.engine.run(task,self.planner)
            return {'route':route,'answer':result,'memory_hits':memories,'execution':execution}
        return {'route':route,'answer':result,'memory_hits':memories}
    def health(self):
        return {'environment':self.runtime.env,'models':list(self.runtime.models.backends),'agents':list(self.runtime.agents.agents),'memory_items':len(self.runtime.memory.data.get('items',[]))}
