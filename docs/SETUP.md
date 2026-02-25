# SYNCIFY — Setup Guide (Day 1)

## Prerequisites

Make sure you have installed:
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js (for future frontend tooling)
- Git

---

## Step 1 — Clone & Environment

```bash
git clone <your-repo-url> syncify
cd syncify
git checkout -b main
```

---

## Step 2 — Python Virtual Environment

```bash
cd backend
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 3 — PostgreSQL Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE syncify_db;
CREATE DATABASE syncify_test;
\q

# Run schema
psql -U postgres -d syncify_db -f ../database/schema.sql
```

---

## Step 4 — Redis

```bash
# Mac
brew install redis
brew services start redis

# Ubuntu/Linux
sudo apt install redis-server
sudo systemctl start redis

# Test Redis is running
redis-cli ping  # Should return PONG
```

---

## Step 5 — Firebase Setup

1. Go to https://console.firebase.google.com
2. Create a new project called "syncify"
3. Enable Authentication → Sign-in methods → Google + Email/Password
4. Go to Project Settings → Service Accounts → Generate new private key
5. Download the JSON file
6. Go to Storage → Get started → Set rules to allow authenticated users

---

## Step 6 — Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your actual values from Firebase.

---

## Step 7 — Run the Server

```bash
cd backend
source venv/bin/activate
python app.py
```

You should see:
```
✅ Firebase initialized
✅ Scheduler initialized
 * Running on http://0.0.0.0:5000
```

---

## Step 8 — Test the API

```bash
# Health check
curl http://localhost:5000/api/health

# Should return:
# {"status": "ok", "service": "syncify-api"}
```

---

## Folder Quick Reference

```
syncify/
├── backend/          ← Flask API (YOU ARE HERE)
├── frontend/         ← HTML/CSS/JS (Day 2-3)
├── database/         ← SQL schema + seeds
└── docs/             ← Documentation
```

---

## Day 1 Checklist

- [ ] Virtual environment created
- [ ] All packages installed
- [ ] PostgreSQL database created
- [ ] Schema.sql executed successfully
- [ ] Redis running
- [ ] Firebase project created
- [ ] .env file configured
- [ ] Flask server starts without errors
- [ ] /api/health returns 200

---

## Common Issues

**psycopg2 install fails:**
```bash
pip install psycopg2-binary
```

**eventlet error on Windows:**
```bash
pip install eventlet==0.33.3
```

**Redis connection refused:**
```bash
redis-server --daemonize yes
```

---

## Git Commit for Day 1

```bash
git add .
git commit -m "Day 1: Project foundation — Flask app, DB schema, auth middleware, WebSocket skeleton"
```

You're done with Day 1. Tomorrow: Database models + User profiles.