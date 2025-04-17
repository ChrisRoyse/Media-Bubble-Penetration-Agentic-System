"""ORM model for raw event ingestion."""
from datetime import datetime
from sqlmodel import SQLModel, Field

class RawEvent(SQLModel, table=True):
    """Database model for a single raw event."""
    id: int | None = Field(default=None, primary_key=True)
    device_id: str
    user_id: str | None = None
    name: str
    ts: datetime
    data: dict | None = None
