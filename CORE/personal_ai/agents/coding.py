
class CodingAgent:
    def __init__(self,models,tools,memory): self.models,self.tools,self.memory=models,tools,memory
    def run(self,query,context=None):
        prompt=f"""Act as a software engineering agent.
First inspect/plan, then propose minimal changes, tests, and rollback points.
Never pretend code was executed unless a tool actually executed it.
Task: {query}
"""
        return self.models.generate([{"role":"user","content":prompt}], capability="reasoning")
