# 🚀 CivicResolve — Quick Start Guide

> **New here? Start here.** This guide gets the API running in under 5 minutes using SQLite — no PostgreSQL or Redis installation required.

---

## 📋 What You Need First

| Tool | Download Link | Why? |
|------|--------------|------|
| **Python 3.11+** | https://www.python.org/downloads/ | Runs the application |
| **Git** | https://git-scm.com/downloads | Downloads the code |

> **Windows users:** When installing Python, tick the checkbox **"Add Python to PATH"** during setup.

---

## ⚡ 5-Minute Setup (Local Dev — No Database Server Needed)

### Step 1 — Download the code

```bash
git clone https://github.com/Hari-kr262/SIH-25031.git
cd SIH-25031
```

### Step 2 — Create a virtual environment

A virtual environment keeps the project's packages separate from your system Python.

```bash
# Create the environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

> You'll know it's active when you see `(venv)` at the start of your terminal prompt.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> ⏳ This takes 2–5 minutes the first time. It downloads all required packages.

### Step 4 — Set up the environment file

```bash
# Copy the example file
cp .env.example .env
```

Now open `.env` in any text editor (Notepad, VS Code, etc.) and change **just these two lines** for local development:

```env
# Change this line:
DATABASE_URL=postgresql://civicresolve:civicresolve123@localhost:5432/civicresolve_db

# To this (uses a simple local file, no database server needed):
DATABASE_URL=sqlite:///./civicresolve.db
```

> Everything else in `.env` can stay as-is for local testing.

### Step 5 — Initialize the database and add sample data

```bash
python database/seed.py
```

This creates the database file and adds sample users, departments, and test data.

### Step 6 — Start the API server

```bash
python main.py
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Step 7 — Open the interactive API docs

Open your browser and go to: **http://localhost:8000/docs**

You'll see the full interactive API documentation where you can test every endpoint!

---

## 🔑 Test Accounts (Created by the Seed Script)

| Role | Email | Password |
|------|-------|---------|
| 🔑 Super Admin | `admin@civicresolve.com` | `admin123` |
| 🏙️ Municipal Admin | `municipal@civicresolve.com` | `admin123` |
| 🏠 Citizen | `rahul@example.com` | `citizen123` |
| 🔧 Field Worker | `worker1@civicresolve.com` | `worker123` |

> ⚠️ **These are test-only passwords. Never use them in production!**

---

## 🧪 Try Your First API Call

### Using the Swagger UI (easiest)

1. Go to http://localhost:8000/docs
2. Click **POST /api/v1/auth/login**
3. Click **"Try it out"**
4. Paste this into the request body:
   ```json
   {
     "email": "rahul@example.com",
     "password": "citizen123"
   }
   ```
5. Click **Execute** — you'll get back a token!

### Using curl (command line)

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "rahul@example.com", "password": "citizen123"}'
```

### Using Python (requests library)

```python
import requests

# Login
resp = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "email": "rahul@example.com",
    "password": "citizen123"
})
token = resp.json()["access_token"]
print("Token:", token)

# List all issues
issues = requests.get("http://localhost:8000/api/v1/issues/").json()
print("Issues:", issues)

# Report a new issue (authenticated)
new_issue = requests.post(
    "http://localhost:8000/api/v1/issues/",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "title": "Pothole on Main Street",
        "category": "pothole",
        "address": "Main Street, Ranchi",
        "description": "Large pothole causing traffic issues"
    }
)
print("Created:", new_issue.json())
```

---

## 🛑 How to Stop the Server

Press **Ctrl+C** in the terminal where the server is running.

---

## 🧪 Run the Tests

```bash
pytest tests/ -v
```

All 46 tests should pass.

---

## 📱 Run the Frontend (Optional)

The frontend is a [Flet](https://flet.dev/) app (Python-based GUI).

```bash
# In a second terminal (with venv activated):
python frontend/app.py
```

The app will open at **http://localhost:8080**

> **Note:** The frontend requires a running API server (Step 6 above) to function.

---

## 🐳 Docker Setup (Alternative — Includes PostgreSQL + Redis)

If you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed, this starts everything with one command:

```bash
docker-compose up -d
```

Then seed the database:

```bash
docker-compose exec app python database/seed.py
```

Services will be available at:
- API: http://localhost:8000/docs
- Database: localhost:5432
- Redis: localhost:6379

To stop:
```bash
docker-compose down
```

---

## ❓ Common Problems & Fixes

### "python is not recognized" (Windows)
Reinstall Python and tick **"Add Python to PATH"** during setup.

### "pip install" fails on a package
Some packages need extra system tools. Try:
```bash
# Windows
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Ubuntu/Debian
sudo apt-get install python3-dev build-essential libpq-dev
pip install -r requirements.txt
```

### "Address already in use" / Port 8000 in use
Change the port:
```bash
uvicorn main:app --reload --port 8001
```
Then access: http://localhost:8001/docs

### Database errors on startup
Delete the old database file and re-seed:
```bash
rm civicresolve.db   # or: del civicresolve.db (Windows)
python database/seed.py
```

### "ModuleNotFoundError"
Make sure your virtual environment is activated (you should see `(venv)` in the prompt), then reinstall:
```bash
pip install -r requirements.txt
```

### The `.env` file is missing
```bash
cp .env.example .env
```

---

## 📂 Key Files at a Glance

```
SIH-25031/
├── main.py               ← Entry point — run this to start the API
├── frontend/app.py       ← Entry point — run this to start the UI
├── requirements.txt      ← All Python packages needed
├── .env.example          ← Template for your configuration
├── database/seed.py      ← Creates test users and sample data
├── tests/                ← Automated tests (run with pytest)
└── docs/                 ← Detailed documentation
```

---

## 📚 More Documentation

| File | Contents |
|------|----------|
| `docs/SETUP_GUIDE.md` | Full setup with PostgreSQL, Redis, production config |
| `docs/API_DOCUMENTATION.md` | All 60+ API endpoints documented |
| `docs/DEPLOYMENT_GUIDE.md` | How to deploy to a server |
| `docs/USER_MANUAL.md` | How to use the application |
| `http://localhost:8000/docs` | Interactive API docs (when server is running) |

---

*Built for Smart India Hackathon 2025 — Problem Statement SIH25031*
*Government of Jharkhand | Clean & Green Technology Theme*
