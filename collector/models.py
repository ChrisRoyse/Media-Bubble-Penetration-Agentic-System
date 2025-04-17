from datetime import datetime
from sqlmodel import SQLModel, Field

class RawEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    device_id: str
    user_id: str | None = None
    name: str
    ts: datetime
    data: dict | None = None
