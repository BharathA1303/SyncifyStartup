You are a Senior Principal Software Architect, AI Systems Engineer, and Startup UI/UX Director.

Build a production-ready, scalable startup-level web platform called:

SYNCIFY

Concept:
Spotify + WhatsApp + Snapchat + AI Emotional Intelligence Platform.

This is NOT a demo.
This is NOT a student project.
This must look like a funded YC-backed startup.

------------------------------------------
CORE PRODUCT VISION
------------------------------------------

SYNCIFY is a real-time music bonding platform that allows users to:

- Stream and share music
- Sync listen with zero delay
- Chat in real-time
- Build streaks and snap-style bonding points
- Analyze compatibility using AI
- Join mood-based public rooms
- Track emotional history through music

------------------------------------------
TECH STACK
------------------------------------------

Frontend:
- HTML5 semantic structure
- CSS3 custom design system
- clamp() used for ALL font sizes and spacing
- CSS variables
- Flexbox + Grid
- No template themes
- Dark modern UI with glassmorphism
- Smooth micro-animations
- Fully responsive (320px → 4K)

JavaScript:
- Modular ES6 architecture
- WebSocket client
- State management pattern
- Optimized audio synchronization

Backend:
- Python Flask
- RESTful API
- Flask-SocketIO
- PostgreSQL
- Redis pub/sub
- Firebase Admin SDK
- JWT authentication
- Rate limiting
- AI service module

------------------------------------------
DATABASE STRUCTURE (EXTENDED & STRONG)
------------------------------------------

Users
- id (UUID)
- firebase_uid
- username
- email
- bio
- profile_picture
- snap_points
- created_at
- updated_at

Friendships
- id
- requester_id
- receiver_id
- status
- streak_count
- last_interaction_date

Songs
- id
- title
- artist
- genre
- mood_tag
- duration
- file_url
- cover_image

Playlists
- id
- user_id
- name
- is_public
- created_at

Playlist_Songs
- id
- playlist_id
- song_id

Conversations
- id
- user1_id
- user2_id

Messages
- id
- conversation_id
- sender_id
- text
- song_id (nullable)
- playlist_id (nullable)
- voice_note_url (nullable)
- created_at

Sync_Sessions
- id
- session_code
- host_id
- guest_id
- song_id
- started_at
- is_private
- is_active

Reactions
- id
- sync_session_id
- user_id
- timestamp_position
- emoji
- created_at

Snap_Transactions
- id
- user1_id
- user2_id
- action_type
- points_added
- created_at

AI_Compatibility
- id
- user1_id
- user2_id
- compatibility_score
- shared_genres
- shared_moods
- listening_overlap_score
- updated_at

AI_Bond_Reports
- id
- user1_id
- user2_id
- weekly_summary_text
- bond_growth_percentage
- dominant_mood
- generated_at

Mood_Rooms
- id
- name
- mood_type
- is_public
- created_at

Mood_Room_Members
- id
- room_id
- user_id

Daily_Challenges
- id
- challenge_type
- description
- reward_points
- created_at

User_Challenge_Progress
- id
- user_id
- challenge_id
- progress_count
- completed

Memory_Timeline
- id
- user1_id
- user2_id
- event_type
- song_id
- description
- created_at

------------------------------------------
FEATURE IMPLEMENTATIONS
------------------------------------------

1️⃣ AI COMPATIBILITY SCORE

When users become friends:

AI analyzes:
- Genre overlap
- Mood similarity
- Listening time overlap
- Frequency of shared songs

Generate:
Soul Sync Score (0–100%)

Store in AI_Compatibility table.

Display:
- Compatibility percentage
- Breakdown visualization
- AI explanation text

------------------------------------------

2️⃣ MOOD-BASED LIVE ROOMS

Predefined rooms:
- Chill
- Study
- Gym
- Party
- Late Night Feels

Features:
- Public sync listening
- Group chat
- Group snap bonus multiplier
- Real-time presence indicator

------------------------------------------

3️⃣ AI BOND ANALYZER

Weekly cron job:
- Analyze interaction frequency
- Shared listening time
- Mood dominance
- Snap growth

Generate:
- Bond growth %
- Emotional summary paragraph
- Suggestions to improve bond

------------------------------------------

4️⃣ DAILY MUSIC CHALLENGES

Examples:
- Share 2 songs today
- Sync listen once
- Create shared playlist

Gamification:
- XP boost
- Streak protection
- Bonus snap multiplier

------------------------------------------

5️⃣ MEMORY TIMELINE

Automatically record:
- First song listened together
- First playlist shared
- Longest sync session
- Highest streak day

Display in visual timeline UI.

------------------------------------------

6️⃣ REAL-TIME REACTIONS DURING SYNC

Users can:
- Tap emoji during playback
- Drop reaction at timestamp
- Highlight favorite moment

Display floating reactions in real-time.

------------------------------------------

7️⃣ PRIVATE LISTENING MODE

Features:
- Encrypted session
- No snap points
- No streak impact
- Hidden from public activity

------------------------------------------

8️⃣ VOICE NOTES INSIDE MUSIC

During sync:
User holds mic → records voice note
Voice note attached to timestamp

Other user hears:
Music continues
Voice plays over at marked time

------------------------------------------

SYNCHRONIZED LISTENING ENGINE

- Server authoritative time
- Latency ping check
- Drift correction algorithm
- Auto realign if >300ms delay
- WebSocket room per session

------------------------------------------

SNAP POINT SYSTEM

+5 Send song
+10 Share playlist
+15 Sync listen
+50 5 consecutive sync
+20 Daily streak
Group mood room multiplier

Bond Levels:
0–100 → New Vibes
100–500 → Music Buddies
500–1500 → Soul Sync
1500+ → Legendary Bond

------------------------------------------

DESIGN SYSTEM RULES

- Dark theme
- Gradient accent:
  linear-gradient(135deg, #7f5af0, #2cb67d)
- Glass blur cards
- 12px border radius
- clamp() typography system
- Smooth hover glow
- Micro animations
- Responsive sidebars collapse to bottom nav on mobile

------------------------------------------

SECURITY

- Firebase token verification
- WebSocket authentication handshake
- Rate limiting
- Sanitized inputs
- Secure file streaming

------------------------------------------

DELIVERABLES

Generate:

- Folder structure
- Full backend Flask API
- WebSocket implementation
- AI service logic
- Database schema (SQL)
- Frontend UI (HTML + CSS clamp system)
- Modular JavaScript
- Snap algorithm functions
- Sync drift correction logic

Make it clean, scalable, modular, production-ready.
This is a startup product.
Architect like a CTO.
Design like Apple.
Engineer like Stripe.