# 🎵 SYNCIFY

> Real-time music bonding platform. Sync. Share. Bond.

Spotify + WhatsApp + Snapchat + AI Emotional Intelligence — all in one.

---

## What is Syncify?

Syncify lets you listen to music in perfect sync with friends, track your
music compatibility using AI, build streaks and bond points, and create
an emotional memory timeline through the songs you share.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask + Flask-SocketIO |
| Database | PostgreSQL |
| Cache / PubSub | Redis |
| Auth | Firebase Admin SDK + JWT |
| Storage | Firebase Storage |
| Frontend | HTML5 + CSS3 + Vanilla JS (ES6 modules) |
| Real-time | WebSocket (SocketIO) |
| Scheduler | APScheduler |

---

## Getting Started

See [docs/SETUP.md](docs/SETUP.md) for full setup instructions.

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Fill in your values
python app.py
```

---

## Features

- 🔄 **Synchronized Listening** — zero-delay music sync with drift correction
- 💬 **Real-time Chat** — share songs, playlists, voice notes in chat
- 🤖 **AI Compatibility** — Soul Sync Score between friends
- ⚡ **Snap Points** — gamified bonding system with streaks
- 🎭 **Mood Rooms** — join public rooms by vibe
- 📅 **Daily Challenges** — earn XP and streak shields
- 🕐 **Memory Timeline** — relive your music moments
- 🔒 **Private Mode** — incognito listening sessions

---

## Project Structure

See [docs/STRUCTURE.md](docs/STRUCTURE.md)

---

## Build Progress

- [x] Day 1 — Foundation, DB Schema, Auth, WebSocket skeleton
- [ ] Day 2 — Database models
- [ ] Day 3 — Design system CSS
- [ ] Day 4 — Landing page
- [ ] Day 5 — Auth UI
- [ ] ...and 44 more days

---

Built with 🎵 and way too much coffee.