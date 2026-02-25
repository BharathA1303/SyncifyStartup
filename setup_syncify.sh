#!/bin/bash

# Create root folder
mkdir -p syncify
cd syncify

# Backend
mkdir -p backend/api
mkdir -p backend/models
mkdir -p backend/services
mkdir -p backend/utils
mkdir -p backend/config

touch backend/app.py
touch backend/config.py
touch backend/extensions.py
touch backend/requirements.txt

touch backend/api/__init__.py
touch backend/api/auth.py
touch backend/api/users.py
touch backend/api/songs.py
touch backend/api/playlists.py
touch backend/api/messages.py
touch backend/api/sync.py
touch backend/api/snaps.py
touch backend/api/rooms.py
touch backend/api/challenges.py
touch backend/api/ai.py

touch backend/models/__init__.py
touch backend/models/user.py
touch backend/models/friendship.py
touch backend/models/song.py
touch backend/models/playlist.py
touch backend/models/message.py
touch backend/models/sync_session.py
touch backend/models/snap.py
touch backend/models/mood_room.py
touch backend/models/challenge.py
touch backend/models/ai_models.py

touch backend/services/__init__.py
touch backend/services/firebase_service.py
touch backend/services/ai_service.py
touch backend/services/snap_service.py
touch backend/services/sync_service.py
touch backend/services/scheduler.py

touch backend/utils/__init__.py
touch backend/utils/auth_middleware.py
touch backend/utils/rate_limiter.py
touch backend/utils/validators.py
touch backend/utils/helpers.py

touch backend/config/__init__.py
touch backend/config/settings.py

# Frontend
mkdir -p frontend/pages
mkdir -p frontend/components
mkdir -p frontend/styles/pages
mkdir -p frontend/js/modules
mkdir -p frontend/js/utils

touch frontend/pages/index.html
touch frontend/pages/login.html
touch frontend/pages/signup.html
touch frontend/pages/dashboard.html
touch frontend/pages/profile.html
touch frontend/pages/friends.html
touch frontend/pages/chat.html
touch frontend/pages/sync.html
touch frontend/pages/playlists.html
touch frontend/pages/rooms.html
touch frontend/pages/challenges.html
touch frontend/pages/timeline.html
touch frontend/pages/compatibility.html

touch frontend/components/player.html
touch frontend/components/nav.html
touch frontend/components/modals.html

touch frontend/styles/design-system.css
touch frontend/styles/components.css
touch frontend/styles/animations.css
touch frontend/styles/layout.css

touch frontend/js/app.js
touch frontend/js/modules/auth.js
touch frontend/js/modules/player.js
touch frontend/js/modules/socket.js
touch frontend/js/modules/sync.js
touch frontend/js/modules/chat.js
touch frontend/js/modules/snaps.js
touch frontend/js/modules/ai.js

touch frontend/js/utils/api.js
touch frontend/js/utils/state.js
touch frontend/js/utils/helpers.js

# Database
mkdir -p database/migrations
touch database/schema.sql
touch database/seeds.sql

# Docs
mkdir -p docs
touch docs/STRUCTURE.md
touch docs/API.md
touch docs/SETUP.md

# Root files
touch .env.example
touch .gitignore
touch README.md

echo "✅ Syncify folder structure created successfully!"