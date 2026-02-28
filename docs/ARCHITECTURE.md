# CivicResolve Architecture

## System Overview

```
Citizens → Flet UI → FastAPI → PostgreSQL
                            → Redis (Celery, Cache)
                            → Cloudinary (Files)
                            → OpenAI (AI)
                            → Twilio (SMS)
                            → SMTP (Email)
```

## Layer Architecture

### 1. Presentation Layer (Flet Frontend)
- Cross-platform Python UI using Material Design 3
- Role-based routing and navigation
- Real-time updates via polling

### 2. API Layer (FastAPI)
- RESTful API with automatic OpenAPI documentation
- JWT authentication + RBAC middleware
- Rate limiting (slowapi)
- 15 route modules covering all features

### 3. Service Layer
- Business logic separated from route handlers
- 12 service modules (auth, issues, voting, etc.)

### 4. Data Layer (SQLAlchemy + PostgreSQL)
- 14 normalized database tables
- Proper relationships with cascades
- Alembic for migrations

### 5. AI/ML Layer
- Image classification (MobileNetV2)
- Text classification (TF-IDF + SVM)
- Urgency prediction
- Fake report detection
- Duplicate detection
- Hotspot prediction

### 6. Background Tasks (Celery + Redis)
- SLA monitoring (hourly)
- Email/SMS notifications (async)
- Report generation (daily)
- Data cleanup (daily)

## Database Schema

```
users (1) ──── (*) issues
users (1) ──── (*) votes
users (1) ──── (*) comments
users (1) ──── (*) notifications
users (1) ──── (*) user_badges
users (*) ──── (1) departments

issues (1) ──── (*) issue_media
issues (1) ──── (1) resolution
issues (1) ──── (*) votes
issues (1) ──── (*) comments

departments (1) ──── (*) issues
departments (1) ──── (1) budget
```

## Security Model

1. **Authentication**: JWT with access + refresh tokens
2. **Authorization**: Role-based (6 roles, hierarchical)
3. **Rate Limiting**: IP-based request throttling
4. **Input Validation**: Pydantic schemas
5. **Audit Logging**: All significant actions recorded
6. **Password Security**: bcrypt hashing

## Scalability

- Stateless API (horizontal scaling)
- Redis caching layer
- Celery for async heavy tasks
- Docker for containerization
- PostgreSQL connection pooling
