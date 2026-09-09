reputation-mvp/
│
├── docker-compose.yml
├── .env
│
├── infrastructure/
│   └── postgres/
│       └── init/
│           └── 01-create-databases.sql
│
└── services/
    ├── api-gateway/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/
    │       └── main.py
    │
    ├── media-service/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── alembic.ini
    │   │
    │   ├── alembic/
    │   │   ├── env.py
    │   │   └── versions/
    │   │       └── 001_create_media.py
    │   │
    │   └── app/
    │       ├── __init__.py
    │       ├── main.py
    │       ├── config.py
    │       ├── db.py
    │       │
    │       ├── api/
    │       │   ├── __init__.py
    │       │   └── media.py
    │       │
    │       ├── models/
    │       │   ├── __init__.py
    │       │   └── media.py
    │       │
    │       ├── messaging/
    │       │   ├── __init__.py
    │       │   ├── broker.py
    │       │   ├── events.py
    │       │   └── handlers.py
    │       │
    │       ├── repositories/
    │       │   ├── __init__.py
    │       │   └── media.py
    │       │
    │       ├── schemas/
    │       │   ├── __init__.py
    │       │   └── media.py
    │       │
    │       └── services/
    │           ├── __init__.py
    │           └── storage.py
    │
    ├── media-processor/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   │
    │   └── app/
    │       ├── __init__.py
    │       ├── main.py
    │       ├── config.py
    │       ├── events.py
    │       ├── storage.py
    │       └── image_processor.py
    │
    ├── review-service/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── alembic.ini
    │   ├── alembic/
    │   └── app/
    │       ├── api/
    │       ├── messaging/
    │       ├── models/
    │       ├── repositories/
    │       ├── schemas/
    │       ├── config.py
    │       ├── db.py
    │       └── main.py
    │
    ├── moderation-service/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/
    │       ├── config.py
    │       ├── events.py
    │       └── main.py
    │
    └── ai-moderation-service/
        ├── Dockerfile
        ├── requirements.txt
        └── app/
            ├── main.py
            ├── schemas.py
            └── graph/
                ├── state.py
                ├── nodes.py
                └── graph.py
