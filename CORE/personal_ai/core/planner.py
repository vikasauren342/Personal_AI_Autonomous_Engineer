from .contracts import Plan
class Planner:
    def __init__(self, models): self.models=models
    def make_plan(self, task):
        prompt=f"""Create a minimal executable plan for this task. Return JSON when possible.\nTask: {task.goal}\nRules: prefer reversible steps; identify required tools; include verification."""
        raw=self.models.generate([{"role":"user","content":prompt}], capability="planning", max_new_tokens=512)
        return Plan(task.id,[{"action":"model_response","content":raw}],[])
