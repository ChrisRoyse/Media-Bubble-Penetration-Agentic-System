"""Centralised, cached settings object"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class _Settings(BaseSettings):
    """Central config. Reads from .env or real env vars."""

    # infra
    KAFKA_BOOTSTRAP: str = "kafka:9092"
    KAFKA_EVENTS_TOPIC: str = "events"
    KAFKA_MATCH_TOPIC: str = "resolved"

    POSTGRES_DSN: str = "postgresql+psycopg2://pg:pg@postgres:5432/pg"
    NEO4J_URI: str = "bolt://neo4j:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASS: str = "neo"

    # external APIs
    OPENAI_API_KEY: str | None = None
    GOOGLE_ADS_CRED_JSON: Path | None = None
    META_APP_ID: str | None = None
    META_APP_SECRET: str | None = None
    META_PAGE_ID: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache(1)
def settings() -> _Settings:
    return _Settings()
