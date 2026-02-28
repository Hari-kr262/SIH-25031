# 🏛️ CivicResolve — SIH 25031

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Flet](https://img.shields.io/badge/Flet-0.21-purple)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-46%20passing-brightgreen)

**Smart India Hackathon 2025 | Problem Statement SIH25031**
**Government of Jharkhand | Clean & Green Technology Theme**

> A complete crowdsourced civic issue reporting and resolution system where citizens report potholes, garbage, broken streetlights, and water leaks — and the government resolves them with full accountability.

---

## 👋 New Here? Start with the Quick Start Guide

> **[📖 QUICKSTART.md](QUICKSTART.md)** — Get the API running in 5 minutes, no database server needed.

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

### Option 1 — Local Dev (No database server required, fastest)

```bash
# 1. Clone and enter the repo
git clone https://github.com/Hari-kr262/SIH-25031.git
cd SIH-25031

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Create your .env file and switch to SQLite
cp .env.example .env
# Open .env and change DATABASE_URL to:
#   DATABASE_URL=sqlite:///./civicresolve.db

# 5. Create the database and add sample data
python database/seed.py

# 6. Start the API server
python main.py
```

API is now running at **http://localhost:8000**
Interactive docs: **http://localhost:8000/docs**

📖 **See [QUICKSTART.md](QUICKSTART.md) for a full step-by-step walkthrough with screenshots, test accounts, and troubleshooting tips.**

### Option 2 — Docker (Includes PostgreSQL + Redis, production-like)

```bash
# Start all services (app + database + redis + celery)
docker-compose up -d

# Add sample data
docker-compose exec app python database/seed.py
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
