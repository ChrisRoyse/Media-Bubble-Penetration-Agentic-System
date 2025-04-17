from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from common.messaging import stream, get_producer
from common.config import settings

model = SentenceTransformer("all-MiniLM-L6-v2")
producer = get_producer()
embeds, raw = [], []
for event in stream(settings().KAFKA_EVENTS_TOPIC, "insight"):
    embeds.append(model.encode(event["name"]))
    raw.append(event)
    if len(embeds) >= 256:
        km = MiniBatchKMeans(n_clusters=8, batch_size=256, random_state=42).fit(np.stack(embeds))
        for idx, lbl in enumerate(km.labels_):
            producer.send(settings().KAFKA_MATCH_TOPIC, {
                "cluster": int(lbl),
                "event": raw[idx],
            })
        embeds.clear(); raw.clear()