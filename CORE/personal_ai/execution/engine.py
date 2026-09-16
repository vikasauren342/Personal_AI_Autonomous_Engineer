from .loop import AutonomousLoop
from personal_ai.core.contracts import Observation, Evaluation

class ExecutionEngine:
    def __init__(self, tools, evaluator, ledger, max_steps=5):
        self.tools,self.evaluator,self.ledger=tools,evaluator,ledger; self.max_steps=max_steps
    def execute_plan(self, plan):
        outputs=[]
        for step in plan.steps:
            if step.get('action')=='tool':
                try: outputs.append(Observation(True,self.tools.call(step['tool'],*step.get('args',[]),**step.get('kwargs',{}))))
                except Exception as e: outputs.append(Observation(False,error=str(e)))
            else: outputs.append(Observation(True,step.get('content')))
        return outputs
    def run(self, task, planner):
        state={'task':task,'steps':[]}
        for i in range(self.max_steps):
            plan=planner.make_plan(task)
            obs=self.execute_plan(plan)
            ev=self.evaluator.evaluate(obs)
            state['steps'].append({'plan':plan,'observations':obs,'evaluation':ev})
            self.ledger.record({'task_id':task.id,'iteration':i,'evaluation':ev.__dict__})
            if ev.done: return state
        return state
