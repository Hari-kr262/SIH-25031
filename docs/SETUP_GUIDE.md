# CivicResolve Setup Guide

> **First time here?** Read **[QUICKSTART.md](../QUICKSTART.md)** first — it gets you running in 5 minutes with no external services.

This guide covers all setup options in detail.

---

## Prerequisites

| Tool | Required Version | Notes |
|------|-----------------|-------|
| Python | 3.11+ | https://www.python.org/downloads/ — tick "Add to PATH" on Windows |
| Git | Any | https://git-scm.com/downloads |
| PostgreSQL | 15+ | Only for Option B / production |
| Redis | 7+ | Only for Celery background tasks |
| Docker Desktop | Any | Only for Docker option |

---

## Option A — Local Dev with SQLite (No extra services needed)

This is the easiest way to run the project and try it out.

### 1. Clone & Install

```bash
git clone https://github.com/Hari-kr262/SIH-25031.git
cd SIH-25031

python -m venv venv
source venv/bin/activate    # Mac/Linux
# venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Configure Environment (SQLite)

```bash
cp .env.example .env
```

Open `.env` and change the `DATABASE_URL` line:

```env
# Change FROM:
DATABASE_URL=postgresql://civicresolve:civicresolve123@localhost:5432/civicresolve_db

# Change TO:
DATABASE_URL=sqlite:///./civicresolve.db
```

All other settings can stay as defaults for local testing.

### 3. Initialize Database and Seed Data

```bash
python database/seed.py
```

This creates all tables and inserts:
- 8 departments (Roads, Water, Electricity, etc.)
- Sample users for every role
- SLA configurations
- Achievement badges

### 4. Start Services

**Terminal 1 — API Server:**
```bash
python main.py
```
API: http://localhost:8000
Interactive docs: http://localhost:8000/docs

**Terminal 2 — Frontend (optional):**
```bash
python frontend/app.py
```
Frontend: http://localhost:8080

> Background tasks (Celery) are not needed for basic development. The API works fully without them.

---

## Option B — Local Dev with PostgreSQL + Redis

Use this when you need to test production-like behavior, Celery tasks, or database-specific features.

### 1. Install Prerequisites

**PostgreSQL (Ubuntu/Debian):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createuser --createdb civicresolve
sudo -u postgres createdb civicresolve_db --owner=civicresolve
sudo -u postgres psql -c "ALTER USER civicresolve WITH PASSWORD 'civicresolve123';"
```

**PostgreSQL (macOS with Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
createuser -s civicresolve
createdb civicresolve_db -O civicresolve
psql -c "ALTER USER civicresolve WITH PASSWORD 'civicresolve123';"
```

**PostgreSQL (Windows):**
Download from https://www.postgresql.org/download/windows/ and use pgAdmin to create the user and database.

**Redis:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis

# Windows — use WSL or Docker
```

### 2. Configure Environment

```bash
cp .env.example .env
# .env already has the PostgreSQL URL, so no change needed
```

### 3. Initialize Database

```bash
python database/seed.py
```

### 4. Start All Services

```bash
# Terminal 1: API server
python main.py

# Terminal 2: Frontend
python frontend/app.py

# Terminal 3: Celery worker (background tasks)
celery -A tasks.celery_app worker --loglevel=info

# Terminal 4: Celery beat (scheduled tasks — SLA checks, etc.)
celery -A tasks.celery_app beat --loglevel=info
```

---

## Option C — Docker (Everything in one command)

### 1. Start All Services

```bash
docker-compose up -d
```

This starts:
- **app** — FastAPI server (port 8000)
- **postgres** — PostgreSQL 15 (port 5432)
- **redis** — Redis 7 (port 6379)
- **celery_worker** — Background task processor
- **celery_beat** — Scheduled task runner

### 2. Seed the Database

```bash
docker-compose exec app python database/seed.py
```

### 3. Useful Docker Commands

```bash
# View running services
docker-compose ps

# View logs
docker-compose logs -f app

# Restart a service
docker-compose restart app

# Stop everything
docker-compose down

# Stop and delete all data (WARNING: destroys database)
docker-compose down -v
```

---

## Test Accounts

| Role | Email | Password |
|------|-------|---------|
| Super Admin | admin@civicresolve.com | admin123 |
| Municipal Admin | municipal@civicresolve.com | admin123 |
| Citizen | rahul@example.com | citizen123 |
| Field Worker | worker1@civicresolve.com | worker123 |

**⚠️ Change all passwords before production deployment!**

---

## Environment Variables Reference

| Variable | Description | Default (local dev) |
|----------|-------------|---------------------|
| `DATABASE_URL` | Database connection | SQLite: `sqlite:///./civicresolve.db` |
| `JWT_SECRET_KEY` | JWT signing secret — **change in production** | `changeme-jwt-secret` |
| `SECRET_KEY` | App secret — **change in production** | `changeme-super-secret-key` |
| `DEBUG` | Enable debug logging | `True` |
| `REDIS_URL` | Redis connection (for Celery) | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | OpenAI — optional, AI features degrade gracefully without it | empty |
| `CLOUDINARY_*` | File storage — optional, files stored locally without it | empty |
| `TWILIO_*` | SMS notifications — optional | empty |
| `SMTP_*` | Email notifications — optional | empty |

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run a specific test file
pytest tests/unit/test_auth.py -v
```

All 46 tests run against SQLite in-memory automatically (no config needed).

---

## Common Problems & Fixes

### "psycopg2 not found" when using SQLite
This happens when `DATABASE_URL` still points to PostgreSQL. Change it to:
```env
DATABASE_URL=sqlite:///./civicresolve.db
```

### "Table already exists" error
Delete the database file and re-seed:
```bash
rm civicresolve.db      # Mac/Linux
del civicresolve.db     # Windows
python database/seed.py
```

### Port 8000 already in use
```bash
uvicorn main:app --reload --port 8001
```

### Permission denied on `venv\Scripts\activate` (Windows)
Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy RemoteSigned
```

### Celery not connecting to Redis
Make sure Redis is running: `redis-cli ping` should return `PONG`.

