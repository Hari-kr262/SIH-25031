# CivicResolve Setup Guide

## Prerequisites
- Python 3.11+
- PostgreSQL 15+ (or Docker)
- Redis 7+ (or Docker)
- Git

## Quick Setup

### 1. Clone & Install
```bash
git clone https://github.com/Hari-kr262/SIH-25031.git
cd SIH-25031
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your PostgreSQL, Redis, and API credentials
```

### 3. Initialize Database
```bash
# Option A: Auto-init on startup (tables created via SQLAlchemy)
uvicorn main:app --reload

# Option B: Manual init
python -c "from database.connection import init_db; init_db()"
```

### 4. Seed Data
```bash
python database/seed.py
```

### 5. Start Services
```bash
# Terminal 1: API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
python frontend/app.py

# Terminal 3: Celery worker (optional)
celery -A tasks.celery_app worker --loglevel=info

# Terminal 4: Celery beat (optional)
celery -A tasks.celery_app beat --loglevel=info
```

## Docker Setup (Recommended)

```bash
# Start all services
docker-compose up -d

# Seed database
docker-compose exec app python database/seed.py

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

## Test Accounts

| Role | Email | Password |
|------|-------|---------|
| Super Admin | admin@civicresolve.com | admin123 |
| Municipal Admin | municipal@civicresolve.com | admin123 |
| Citizen | rahul@example.com | citizen123 |
| Field Worker | worker1@civicresolve.com | worker123 |

**⚠️ Change all passwords before production deployment!**

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | localhost |
| REDIS_URL | Redis connection string | localhost |
| JWT_SECRET_KEY | JWT signing secret | changeme |
| OPENAI_API_KEY | OpenAI API key | empty |
| CLOUDINARY_* | File storage credentials | empty |
| TWILIO_* | SMS credentials | empty |
| SMTP_* | Email credentials | empty |

## Running Tests

```bash
pytest tests/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v
```
