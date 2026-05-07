
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ingest, analytics, lti

app = FastAPI(title="EduSense API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(analytics.router)
app.include_router(lti.router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
