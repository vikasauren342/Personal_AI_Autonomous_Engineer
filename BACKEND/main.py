from fastapi import FastAPI
from pydantic import BaseModel

from CORE.personal_ai.bootstrap import Bootstrap
from CORE.personal_ai.core.orchestrator import Orchestrator

app = FastAPI(
    title="Personal AI",
    version="3.1.0",
)


class ChatRequest(BaseModel):
    query: str
    autonomous: bool = False


runtime = Bootstrap().start()
orchestrator = Orchestrator(runtime)


@app.get("/health")
def health():
    return orchestrator.health()


@app.post("/chat")
def chat(request: ChatRequest):
    return orchestrator.ask(
        request.query,
        autonomous=request.autonomous,
    )