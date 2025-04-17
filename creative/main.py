import asyncio
import json
from openai import AsyncOpenAI
from common.messaging import stream, get_producer
from common.config import settings

cfg = settings()
client = AsyncOpenAI()
producer = get_producer()

PROMPT_TMPL = (
    "You are an awardwinning ad creative. Given the following product and user cluster, write "
    "a 40character headline, 90char description, and suggest an emoji that resonates."
    "\n\nINPUT:\n{data}\n\nOUTPUT in JSON with keys: headline, desc, emoji."
)

async def create(asset: dict):
    msg = PROMPT_TMPL.format(data=json.dumps(asset))
    rsp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": msg}],
    )
    j = json.loads(rsp.choices[0].message.content)
    return {**asset, **j}

async def main():
    async for ev in stream(cfg.KAFKA_MATCH_TOPIC, "creative"):
        enriched = await create(ev)
        producer.send("creative-ready", enriched)

if __name__ == "__main__":
    asyncio.run(main())
