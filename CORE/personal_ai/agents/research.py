
class ResearchAgent:
    def __init__(self,models,tools,memory): self.models,self.tools,self.memory=models,tools,memory
    def run(self,query,context=None):
        prompt=f"""Act as a research planner and synthesizer.
Break the task into evidence questions, identify what must be verified,
separate facts from inference, and produce a structured research plan.
Do not invent web evidence. Task: {query}
Relevant memory: {context or {}}
"""
        return self.models.generate([{"role":"user","content":prompt}], capability="reasoning")
