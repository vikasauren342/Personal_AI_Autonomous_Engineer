from fastapi import FastAPI

app = FastAPI(
    title="Personal AI",
    version="3.1.0",
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "personal-ai",
        "version": "3.1.0",
    }
