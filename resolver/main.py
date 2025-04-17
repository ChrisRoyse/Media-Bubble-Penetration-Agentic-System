import json
import itertools
from kafka import KafkaConsumer
from neo4j import GraphDatabase
from common.config import settings

CFG = settings()
consumer = KafkaConsumer(
    CFG.KAFKA_EVENTS_TOPIC,
    bootstrap_servers=CFG.KAFKA_BOOTSTRAP,
    value_deserializer=lambda m: json.loads(m.decode()),
    group_id="resolver",
    max_poll_records=500,
)

driver = GraphDatabase.driver(CFG.NEO4J_URI, auth=(CFG.NEO4J_USER, CFG.NEO4J_PASS))
CYPHER = (
    "UNWIND $events AS e "
    "MERGE (d:Device {id:e.device}) "
    "FOREACH(u IN CASE WHEN e.uid IS NULL THEN [] ELSE [e.uid] END | "
    "  MERGE (p:Person {id:u}) MERGE (p)-[:USES]->(d)) "
    "CREATE (d)-[:HAS_EVENT]->(:Event {name:e.name, ts:datetime(e.ts), data:e.data})"
)

def batched(it, size=200):
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk

with driver.session() as sess:
    for chunk in batched(consumer):
        payload = [{
            "device": e.value["device_id"],
            "uid": e.value.get("user_id"),
            "name": e.value["name"],
            "ts": e.value["ts"],
            "data": json.dumps(e.value["data"]),
        } for e in chunk]
        sess.run(CYPHER, events=payload)