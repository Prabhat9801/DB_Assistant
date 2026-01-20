# DB Assistant Backend

A **read-only** database chatbot API with **hardcoded security** that cannot be bypassed even if the LLM hallucinates.

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: API Validation (Pydantic)                         │
│  ├── Request size limits                                    │
│  ├── Input sanitization                                     │
│  └── Field validation                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: LLM generates SQL                                 │
│  ├── Schema-aware prompting                                 │
│  ├── ENUM value injection                                   │
│  └── Table name validation                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  🔒 LAYER 3: HARDCODED SECURITY VALIDATION                  │
│  ├── Length check (max 2000 chars)                          │
│  ├── Whitelist check (SELECT only)                          │
│  ├── Blocked keyword detection (40+ keywords)               │
│  ├── Blocked pattern detection (regex)                      │
│  └── Multiple statement detection                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
        BLOCKED              ALLOWED
            │                   │
            ▼                   ▼
    ❌ Return Error      ✅ Execute Query
```

## 🚫 Hardcoded Blocked Keywords (40+)

The following keywords are **PERMANENTLY BLOCKED** and **CANNOT be bypassed**:

- **Data Modification**: DELETE, UPDATE, INSERT, MERGE, UPSERT, REPLACE
- **Data Definition**: DROP, ALTER, CREATE, TRUNCATE, RENAME
- **Permissions**: GRANT, REVOKE, DENY
- **Transactions**: COMMIT, ROLLBACK, SAVEPOINT
- **Administration**: VACUUM, ANALYZE, REINDEX, CLUSTER
- **Dangerous Functions**: EXEC, EXECUTE, CALL, PREPARE
- **System Operations**: COPY, PG_DUMP, PG_RESTORE, LOAD
- **File Operations**: PG_READ_FILE, PG_WRITE_FILE, LO_IMPORT, LO_EXPORT

## 📁 Project Structure

```
Backend/
├── src/
│   ├── main.py                  # FastAPI entry point
│   ├── config/                  # Configuration settings
│   ├── api/routes/              # API endpoints
│   │   ├── chat.py              # Chat endpoints
│   │   └── health.py            # Health check
│   ├── core/
│   │   ├── security.py          # 🔒 HARDCODED SECURITY
│   │   └── exceptions.py        # Custom exceptions
│   └── services/
│       ├── chat_service.py      # Main orchestration
│       ├── db_service.py        # Database operations
│       └── schema_service.py    # Dynamic schema discovery
├── .env.example                 # Environment template
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your database and OpenAI credentials
```

### 3. Run the Server
```bash
uvicorn src.main:app --reload --port 8000
```

### 4. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Send a query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all users"}'
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Process natural language query |
| GET | `/chat/tables` | List allowed tables |
| GET | `/chat/schema` | Get database schema |
| POST | `/chat/config/tables` | Add/remove allowed tables |
| GET | `/health` | Health check |

## 🌐 Language Support

- **English**: All queries supported
- **Hinglish**: Hindi-English mix queries supported

## 📊 Example Queries

```json
// English
{"question": "Show me all active users"}

// Hinglish  
{"question": "Sabhi active users dikhao"}

// Complex
{"question": "How many tasks are completed this week?"}
```

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | - |
| `DB_PORT` | PostgreSQL port | 5432 |
| `DB_NAME` | Database name | - |
| `DB_USER` | Database user | - |
| `DB_PASSWORD` | Database password | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENAI_MODEL` | OpenAI model | gpt-4o-mini |
| `SCHEMA_CACHE_TTL_MINUTES` | Schema cache duration | 5 |

## 🔐 Security Notes

1. **Blocked keywords are HARDCODED** in `src/core/security.py`
2. They **CANNOT be modified** via environment variables
3. Even if LLM generates malicious SQL, it will be **BLOCKED**
4. Only **SELECT** queries are allowed
5. Maximum query length: **2000 characters**