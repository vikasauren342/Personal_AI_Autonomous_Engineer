
from .research import ResearchAgent
from .coding import CodingAgent
from .general import GeneralAgent
class AgentRegistry:
    def __init__(self, root, models, tools, memory):
        self.agents={
            "research":ResearchAgent(models,tools,memory),
            "coding":CodingAgent(models,tools,memory),
            "general":GeneralAgent(models,tools,memory),
        }
    def get(self,name): return self.agents.get(name,self.agents["general"])
