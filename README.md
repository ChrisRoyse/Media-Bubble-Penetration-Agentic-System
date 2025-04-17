<<<<<<< HEAD
# Media Bubble Penetration Agentic System

This monorepo contains all micro‑services needed to collect consented cross‑device signals, resolve identities, generate personalised creatives, push them into the major ad networks, and measure lift—while enforcing modern privacy rules.

## Directory layout
```
.
├── docker-compose.yml
├── common/
│   ├── config.py
│   ├── messaging.py
│   └── storage.py
├── collector/
│   ├── main.py
│   └── models.py
├── resolver/
│   ├── main.py
│   └── graph.py
├── insight/
│   ├── main.py
│   └── embedding.py
├── creative/
│   ├── main.py
│   └── generator.py
├── placement/
│   ├── main.py
│   ├── google_client.py
│   └── meta_client.py
├── measurement/
│   └── main.py
└── compliance/
    └── middleware.py
```

## Environment Variables
- **KAFKA_BOOTSTRAP**: Kafka bootstrap server (default: `kafka:9092`)
- **KAFKA_EVENTS_TOPIC**: Kafka topic for raw events (default: `events`)
- **KAFKA_MATCH_TOPIC**: Kafka topic for clustered/matched events (default: `resolved`)
- **NEO4J_URI**: Neo4j connection URI (default: `bolt://neo4j:7687`)
- **NEO4J_USER**: Neo4j username (default: `neo4j`)
- **NEO4J_PASS**: Neo4j password (default: `neo`)
- **POSTGRES_DSN**: Postgres DSN (default: `postgresql+psycopg2://pg:pg@postgres:5432/pg`)
- **OPENAI_API_KEY**: (Optional) OpenAI API key for creative/insight agents
- **GOOGLE_ADS_CRED_JSON**: (Optional) Path to Google Ads API credentials JSON
- **META_APP_ID**: (Optional) Meta app ID for Meta client
- **META_APP_SECRET**: (Optional) Meta app secret for Meta client

You can set these in a `.env` file at the root of the repo.

## Running the System

To build and start all services:

```sh
docker compose up --build
```

This will start all required services and agents. Each agent will connect to the appropriate dependencies as defined in `docker-compose.yml`.

## Notes
- All services are written in Python and expect the dependencies defined in their respective Dockerfiles (not included here).
- For development, ensure you have Docker and Docker Compose v2+ installed.
- For production, configure secrets and credentials securely.
=======
# Media-Bubble-Penetration-Agentic-System
>>>>>>> 4912473bf58e2dd0782d5d4e9b3298cee0fe0c0f
