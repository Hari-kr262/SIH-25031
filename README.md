# 🏛️ CivicResolve — SIH 25031

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Flet](https://img.shields.io/badge/Flet-0.21-purple)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Smart India Hackathon 2025 | Problem Statement SIH25031**
**Government of Jharkhand | Clean & Green Technology Theme**

> A complete crowdsourced civic issue reporting and resolution system where citizens report potholes, garbage, broken streetlights, and water leaks — and the government resolves them with full accountability.

---

## ✨ Features

- 📸 **Multi-media Issue Reporting** — Photo, video, voice, and text
- 🗺️ **Interactive Maps** — Real-time issue heatmaps and cluster views
- 🤖 **AI-Powered** — Auto-categorization, duplicate detection, fake report detection
- 🏆 **Gamification** — Points, badges, leaderboards for citizen engagement
- 📊 **Analytics Dashboard** — SLA tracking, performance metrics, budget management
- 🔔 **Smart Notifications** — Email, SMS, and in-app notifications
- 🌐 **Multi-language** — English, Hindi, and regional language support
- 👥 **6 User Roles** — Full RBAC from citizens to super admin
- 📱 **Cross-platform UI** — Built with Flet (Material Design 3)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI + Uvicorn |
| Database | PostgreSQL + SQLAlchemy + Alembic |
| Authentication | JWT (PyJWT) + bcrypt (passlib) |
| Frontend | Flet (Material Design 3) |
| AI/ML | OpenAI API + scikit-learn + TensorFlow/Keras |
| Maps | Folium + geopy |
| Charts | Plotly |
| Notifications | SMTP + Twilio |
| File Storage | Cloudinary |
| Export | ReportLab (PDF) + openpyxl (Excel) |
| Background Tasks | Celery + Redis |
| Deployment | Docker + docker-compose |

---

## 👥 User Roles

| Role | Description |
|------|-------------|
| 🏠 **Citizen** | Report issues, vote, verify fixes, earn gamification rewards |
| 🤝 **Community Volunteer** | Ground verification, trusted validator (2x vote weight) |
| 🔧 **Field Worker** | Fix issues, upload geo-verified proof, SLA-bound |
| 🏢 **Department Head** | Manage workers, assign issues, track budget |
| 🏙️ **Municipal Admin** | Oversee all departments, analytics, moderation |
| ⚡ **Super Admin** | System config, audit logs, feature flags |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Local Setup

```bash
# 1. Clone repository
git clone https://github.com/Hari-kr262/SIH-25031.git
cd SIH-25031

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Run database migrations
alembic upgrade head

# 6. Seed initial data
python database/seed.py

# 7. Start the API server
uvicorn main:app --reload

# 8. Start the frontend (new terminal)
python frontend/app.py
```

### Docker Setup (Recommended)

```bash
# Start all services
docker-compose up -d

# Seed database
docker-compose exec app python database/seed.py

# View logs
docker-compose logs -f app
```

**Default Admin Credentials:**
- Email: `admin@civicresolve.com`
- Password: `admin123`
- 🔴 **Change these immediately in production!**

---

## 📁 Project Structure

```
CivicResolve/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker services
├── config/                    # Configuration management
├── backend/                   # FastAPI backend
│   ├── models/                # SQLAlchemy ORM models (14 tables)
│   ├── schemas/               # Pydantic validation schemas
│   ├── routes/                # API route handlers (15 modules)
│   ├── services/              # Business logic (12 modules)
│   ├── middleware/            # Auth, RBAC, rate limiting
│   └── utils/                 # Helper utilities
├── ai/                        # AI/ML components
├── frontend/                  # Flet UI application
│   ├── citizen/               # Citizen screens
│   ├── volunteer/             # Volunteer screens
│   ├── worker/                # Field worker screens
│   ├── department_head/       # Department head screens
│   ├── admin/                 # Municipal admin screens
│   └── super_admin/           # Super admin screens
├── tasks/                     # Celery background tasks
├── database/                  # DB connection & seed data
├── tests/                     # Unit & integration tests
└── docs/                      # Documentation
```

---

## 🗺️ Issue Categories

- 🕳️ Pothole | 🗑️ Garbage | 💡 Streetlight | 💧 Water Leak
- 🌊 Drainage | 🛣️ Road Damage | 🚮 Illegal Dumping | 🌳 Fallen Tree
- 💩 Sewage | 🏛️ Public Property | 📋 Other

## ⏱️ SLA Defaults

| Category | Deadline |
|----------|---------|
| Water Leak | 12 hours |
| Garbage | 24 hours |
| Pothole | 48 hours |
| Drainage | 48 hours |
| Streetlight | 72 hours |

---

## 🏆 Gamification

**Points System:**
- Report Issue: +10 pts | Verified Report: +5 pts
- Upvote: +2 pts | Verify Resolution: +5 pts
- Volunteer Verify: +15 pts | Volunteer Fix: +25 pts
- Fake Report Penalty: -20 pts

**Citizen Levels:**
- 🌱 Newcomer (0-50) → 👤 Active Citizen (51-200) → 🏅 Community Champion (201-500) → 🎖️ Civic Leader (501-1000) → 🏆 City Hero (1000+)

---

## 🌈 Color Scheme

- **Primary:** Civic Blue `#1565C0`
- **Success:** Government Green `#2E7D32`
- **Warning:** Alert Amber `#F57F17`
- **Error:** Critical Red `#C62828`

---

## 📄 License

MIT License — Built for Smart India Hackathon 2025

---

*Built with ❤️ for the citizens of Jharkhand*
