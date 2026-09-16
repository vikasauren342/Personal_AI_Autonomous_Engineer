
class AutonomousLoop:
    """Bounded plan -> execute -> evaluate -> repair loop. Never unbounded by default."""
    def __init__(self, planner, executor, evaluator, max_steps=5):
        self.planner,self.executor,self.evaluator=planner,executor,evaluator
        self.max_steps=max_steps
    def run(self, task):
        state={"task":task,"steps":[]}
        for i in range(self.max_steps):
            plan=self.planner(state)
            result=self.executor(plan)
            state["steps"].append({"plan":plan,"result":result})
            verdict=self.evaluator(state)
            if verdict.get("done"): return state
            state["feedback"]=verdict
        return state
