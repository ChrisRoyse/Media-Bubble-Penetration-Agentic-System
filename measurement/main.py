import time, json, random
from common.messaging import get_producer
from collections import defaultdict

producer = get_producer()
lifts = defaultdict(int)

def mock_topics_report():  # placeholder for Privacy Sandbox
    return {"cluster": random.randint(0, 7), "conv": random.randint(0, 3)}

def mock_skan_postback():
    return {"cluster": random.randint(0, 7), "conv": 1}

while True:
    # pretend we received reports
    for rep in (mock_topics_report(), mock_skan_postback()):
        lifts[str(rep["cluster"])] += rep["conv"]
    if int(time.time()) % 300 == 0:
        producer.send("lift-metrics", json.loads(json.dumps(lifts)))
        print("[Measure] lift sent", lifts)
    time.sleep(8)