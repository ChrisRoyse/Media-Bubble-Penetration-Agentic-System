from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
from common.config import settings

engine = create_engine(settings().POSTGRES_DSN, echo=False, pool_pre_ping=True)


def init_db() -> None:
    """Create tables once on collector startup."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def session_scope():
    with Session(engine) as sess:
        yield sess
