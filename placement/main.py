import asyncio
import json
import logging
from openai import AsyncOpenAI
from common.messaging import stream, get_producer
from common.config import settings

logging.basicConfig(level=logging.INFO)
client = AsyncOpenAI()
producer = get_producer()
cfg = settings()

PROMPT = (
    "You are an elite ad copywriter. Based on the CLUSTER and EVENT below, output JSON with:\n"
    "headline (≤40 chars), description (≤90), emoji, and an image_prompt string for a 1:1 creative.\n"
    "CLUSTER: {cluster}\nEVENT: {event}\nJSON:"
)

async def enrich(payload: dict):
    msg = PROMPT.format(cluster=payload["cluster"], event=json.dumps(payload["event"]))
    rsp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": msg}],
    )
    creative = json.loads(rsp.choices[0].message.content)
    # generate image bytes (DALL·E)
    img_rsp = await client.images.generate(
        prompt=creative["image_prompt"], n=1, size="512x512", response_format="b64_json")
    creative["image_b64"] = img_rsp.data[0].b64_json
    return creative

async def main():
    async for item in stream(cfg.KAFKA_MATCH_TOPIC, "creative"):
        enriched = await enrich(item)
        producer.send("creative-ready", enriched)
        logging.info("Creative ready for placement – cluster %s", item["cluster"])

if __name__ == "__main__":
    asyncio.run(main())