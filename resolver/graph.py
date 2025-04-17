from neo4j import GraphDatabase
from common.config import settings

_cfg = settings()
_driver = GraphDatabase.driver(_cfg.NEO4J_URI, auth=(_cfg.NEO4J_USER, _cfg.NEO4J_PASS))


def interests_for_person(pid: str) -> list[str]:
    with _driver.session() as s:
        q = "MATCH (p:Person {id:$pid})-[:HAS_EVENT]->(e:Event) RETURN e.name as n LIMIT 100"
        rs = s.run(q, pid=pid)
        return [r["n"] for r in rs]
