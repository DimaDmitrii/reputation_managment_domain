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
        └── app/
            └── main.py
