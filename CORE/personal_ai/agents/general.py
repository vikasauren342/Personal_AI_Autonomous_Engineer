
class GeneralAgent:
    def __init__(self,models,tools,memory): self.models,self.tools,self.memory=models,tools,memory
    def run(self,query,context=None):
        prompt=f"""You are the user's local Personal AI.
Use memory/context when useful. Be explicit about uncertainty.
Do not claim to have executed tools unless you actually did.
Task: {query}
Context: {context or {}}
"""
        return self.models.generate([{"role":"user","content":prompt}], capability="chat")
