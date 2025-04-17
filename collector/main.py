from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from collector.models import RawEvent
from common.messaging import get_producer
from common.storage import init_db, session_scope
from common.config import settings
from compliance.middleware import ConsentMiddleware

app = FastAPI(title="Collector")
app.add_middleware(ConsentMiddleware)
producer = get_producer()
init_db()

class Event(BaseModel):
    device_id: str = Field(..., example="abc123-ios")
    user_id: str | None = Field(None, example="user@example.com")
    name: str = Field(..., example="page_view")
    ts: datetime = Field(default_factory=datetime.utcnow)
    data: dict = Field(default_factory=dict)

@app.post("/event")
async def ingest(evt: Event):
    # store in DB
    with session_scope() as sess:
        sess.add(RawEvent(**evt.model_dump()))
        sess.commit()
    # stream to Kafka
    try:
        producer.send(settings().KAFKA_EVENTS_TOPIC, evt.model_dump())
    except Exception as exc:  # pragma: no cover
        raise HTTPException(500, f"Kafka error: {exc}") from exc
    return {"status": "queued"}

if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)