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
    ├── review-service/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/
    │       └── main.py
    │
    └── media-service/
        ├── Dockerfile
        ├── requirements.txt
        ├── alembic.ini
        │
        ├── alembic/
        │   ├── env.py
        │   └── versions/
        │       └── 001_create_media.py
        │
        └── app/
            ├── __init__.py
            ├── main.py
            ├── config.py
            ├── db.py
            │
            ├── api/
            │   ├── __init__.py
            │   └── media.py
            │
            ├── models/
            │   ├── __init__.py
            │   └── media.py
            │
            ├── repositories/
            │   ├── __init__.py
            │   └── media.py
            │
            ├── schemas/
            │   ├── __init__.py
            │   └── media.py
            │
            └── services/
                ├── __init__.py
                └── storage.py
