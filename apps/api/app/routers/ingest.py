from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
from typing import Optional, List
import asyncpg, json
from datetime import datetime

router = APIRouter()

class LearnerStateEvent(BaseModel):
    session_id: str
    learner_id: str
    consent_scope: List[str]
    learner_state: Optional[str] = None
    state_confidence: Optional[float] = None
    timestamp: Optional[str] = None
    content_id: Optional[str] = None
    section_id: Optional[str] = None
    privacy_class: Optional[str] = "behavioral"
    signals: Optional[dict] = None

@router.websocket("/ws/ingest")
async def websocket_ingest(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            event = LearnerStateEvent(**data)
        except Exception as e:
            await websocket.send_text(f"Invalid JSON: {e}")
            continue

        if not event.consent_scope:
            await websocket.send_text("Consent scope empty. Denied.")
            continue

        conn = None
        try:
            conn = await asyncpg.connect(
                user="edusense", password="edusense_dev",
                database="edusense", host="localhost"
            )
            await conn.execute("""
                INSERT INTO learner_events
                  (id, session_id, learner_id, content_id, section_id,
                   timestamp, learner_state, state_confidence, signals,
                   privacy_class, consent_scope)
                VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            """,
                event.session_id, event.learner_id,
                event.content_id, event.section_id,
                datetime.fromisoformat(event.timestamp.replace('Z','+00:00')) if event.timestamp else datetime.utcnow(),
                event.learner_state, event.state_confidence,
                json.dumps(event.signals or {}),
                event.privacy_class, event.consent_scope
            )
            await websocket.send_text("ok")
        except Exception as e:
            await websocket.send_text(f"DB error: {e}")
        finally:
            if conn:
                await conn.close()
