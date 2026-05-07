from fastapi import FastAPI
from app.routers import ingest

app = FastAPI(title="EduSense API", version="0.1.0")

app.include_router(ingest.router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
