from __future__ import annotations
import json
from typing import Iterator
from kafka import KafkaProducer, KafkaConsumer
from common.config import settings

_PRODUCER: KafkaProducer | None = None


def _init_producer() -> KafkaProducer:
    cfg = settings()
    return KafkaProducer(
        bootstrap_servers=cfg.KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v, default=str).encode(),
        acks="all",
        linger_ms=10,
        batch_size=64_000,
    )

def get_producer() -> KafkaProducer:
    global _PRODUCER  # pylint: disable=global-statement
    if _PRODUCER is None:
        _PRODUCER = _init_producer()
    return _PRODUCER

def get_consumer(topic: str, group: str) -> KafkaConsumer:  # type: ignore
    cfg = settings()
    return KafkaConsumer(
        topic,
        bootstrap_servers=cfg.KAFKA_BOOTSTRAP,
        group_id=group,
        value_deserializer=lambda m: json.loads(m.decode()),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=1_000,
    )

def stream(topic: str, group: str) -> Iterator[dict]:
    consumer = get_consumer(topic, group)
    for msg in consumer:
        yield msg.value
