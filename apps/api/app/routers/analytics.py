from fastapi import APIRouter
import asyncpg

router = APIRouter()

@router.get("/api/v1/events")
async def get_events(limit: int = 20):
    conn = await asyncpg.connect(
        user="edusense", password="edusense_dev",
        database="edusense", host="localhost"
    )
    try:
        rows = await conn.fetch(
            "SELECT session_id, learner_id, learner_state, state_confidence, timestamp, privacy_class "
            "FROM learner_events ORDER BY timestamp DESC LIMIT $1", limit
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()
