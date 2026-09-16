class Router:
    """Capability router. Model/tool availability is decided elsewhere."""
    def __init__(self,registry,agents,memory): self.registry,self.agents,self.memory=registry,agents,memory
    def route(self,query):
        q=query.lower()
        if any(x in q for x in ['code','coding','program','debug','python','software','api','script']): return 'coding'
        if any(x in q for x in ['research','investigate','compare','evidence','study','what is','why']): return 'research'
        return 'general'
