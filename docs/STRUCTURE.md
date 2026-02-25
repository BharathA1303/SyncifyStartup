# SYNCIFY — Project Structure

```
syncify/
├── backend/
│   ├── app.py                  # Flask app entry point
│   ├── config.py               # Environment config
│   ├── extensions.py           # Flask extensions (db, socketio, redis)
│   ├── requirements.txt        # Python dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py             # Auth routes
│   │   ├── users.py            # User profile routes
│   │   ├── songs.py            # Song upload/fetch routes
│   │   ├── playlists.py        # Playlist routes
│   │   ├── messages.py         # Chat routes
│   │   ├── sync.py             # Sync session routes
│   │   ├── snaps.py            # Snap point routes
│   │   ├── rooms.py            # Mood room routes
│   │   ├── challenges.py       # Daily challenge routes
│   │   └── ai.py               # AI service routes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── friendship.py
│   │   ├── song.py
│   │   ├── playlist.py
│   │   ├── message.py
│   │   ├── sync_session.py
│   │   ├── snap.py
│   │   ├── mood_room.py
│   │   ├── challenge.py
│   │   └── ai_models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── firebase_service.py  # Firebase Admin SDK
│   │   ├── ai_service.py        # AI compatibility + bond
│   │   ├── snap_service.py      # Snap point engine
│   │   ├── sync_service.py      # Sync engine logic
│   │   └── scheduler.py         # Cron jobs
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py   # JWT verification
│   │   ├── rate_limiter.py      # Rate limiting
│   │   ├── validators.py        # Input sanitization
│   │   └── helpers.py           # Utility functions
│   └── config/
│       ├── __init__.py
│       └── settings.py          # App settings by env
├── frontend/
│   ├── pages/
│   │   ├── index.html           # Landing page
│   │   ├── login.html           # Auth page
│   │   ├── signup.html          # Signup page
│   │   ├── dashboard.html       # Main app shell
│   │   ├── profile.html         # User profile
│   │   ├── friends.html         # Friends system
│   │   ├── chat.html            # Messaging
│   │   ├── sync.html            # Sync listening
│   │   ├── playlists.html       # Playlists
│   │   ├── rooms.html           # Mood rooms
│   │   ├── challenges.html      # Daily challenges
│   │   ├── timeline.html        # Memory timeline
│   │   └── compatibility.html   # AI compatibility
│   ├── components/
│   │   ├── player.html          # Music player component
│   │   ├── nav.html             # Navigation
│   │   └── modals.html          # Reusable modals
│   ├── styles/
│   │   ├── design-system.css    # Variables + tokens
│   │   ├── components.css       # Reusable components
│   │   ├── animations.css       # All animations
│   │   ├── layout.css           # Grid + flex layouts
│   │   └── pages/               # Page-specific styles
│   └── js/
│       ├── app.js               # App entry point
│       ├── modules/
│       │   ├── auth.js          # Firebase auth
│       │   ├── player.js        # Audio player
│       │   ├── socket.js        # WebSocket client
│       │   ├── sync.js          # Sync engine client
│       │   ├── chat.js          # Chat module
│       │   ├── snaps.js         # Snap system
│       │   └── ai.js            # AI features
│       └── utils/
│           ├── api.js           # API client
│           ├── state.js         # State management
│           └── helpers.js       # Utility functions
├── database/
│   ├── schema.sql               # Full DB schema
│   ├── seeds.sql                # Seed data
│   └── migrations/              # Future migrations
├── docs/
│   ├── STRUCTURE.md             # This file
│   ├── API.md                   # API documentation
│   └── SETUP.md                 # Setup guide
├── .env.example                 # Environment variables template
├── .gitignore
└── README.md
```