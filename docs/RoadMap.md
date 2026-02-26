PHASE 1 — Foundation & Design System
Week 1 (Days 1–7)
Day 1 — Project Setup & Architecture
Set up your entire folder structure, Git repository, Python virtual environment, Flask app skeleton, and PostgreSQL database connection. By end of day you have a running blank Flask server and connected database. Time: 6hrs.
Day 2 — Database Schema
Write all SQL CREATE TABLE statements from the full schema. Users, Friendships, Songs, Playlists, Messages, Sync_Sessions, Reactions, Snap_Transactions, AI_Compatibility, Mood_Rooms, Memory_Timeline. Run migrations. Verify all tables exist. Time: 6hrs.
Day 3 — Design System (CSS)
Build your entire CSS foundation. Variables, clamp() typography, glassmorphism card system, gradient accents, button styles, input styles, animation keyframes. This file becomes your design bible for every page. Time: 6hrs.
Day 4 — Landing Page UI
Build the public landing page. Hero section, features section, how it works, mood rooms preview, CTA. Must look funded and professional. This is your first impression. Time: 6hrs.
Day 5 — Authentication UI
Build Login page and Signup page. Firebase Auth frontend integration. Google sign-in button, email/password form, animated transitions between login and signup. Time: 6hrs.
Day 6 — Firebase Auth Backend
Flask route to verify Firebase ID tokens using Firebase Admin SDK. JWT generation after verification. User creation in PostgreSQL on first login. Middleware for protected routes. Time: 6hrs.
Day 7 — Dashboard Shell + Navigation
Build the main app shell. Sidebar navigation (desktop), bottom nav (mobile), header bar, responsive layout grid. Empty content area placeholder. This is the frame every other page lives inside. Time: 6hrs.

PHASE 2 — Core User Features
Week 2 (Days 8–14)
Day 8 — User Profile Page
Profile UI with avatar, username, bio, snap points display, bond level badge, stats. Edit profile form. Backend API routes: GET /profile, PUT /profile. Profile picture upload to Firebase Storage. Time: 6hrs.
Day 9 — Friends System Backend
API routes: send friend request, accept/reject, list friends, list pending requests. Friendship table logic. Streak tracking setup. Time: 6hrs.
Day 10 — Friends System Frontend
Friends page UI. Search users, send requests, pending requests inbox, friends list with snap point display, bond level indicators. Time: 6hrs.
Day 11 — Music Upload & Song Model
Song upload form. File stored in Firebase Storage. Metadata saved to Songs table. Genre and mood tagging on upload. Backend routes: POST /songs, GET /songs, GET /songs/:id. Time: 6hrs.
Day 12 — Music Player Component
Build the core audio player UI. Waveform-style progress bar, play/pause, skip, volume, song info display, cover art. This is a reusable component used everywhere in the app. Time: 6hrs.
Day 13 — Playlist System Backend
API routes: create playlist, add song, remove song, get playlist, list user playlists, make public/private. Playlist_Songs join table logic. Time: 6hrs.
Day 14 — Playlist System Frontend
Playlist page UI. Create playlist modal, playlist grid view, song list inside playlist, drag to reorder, share playlist button. Time: 6hrs.

PHASE 3 — Real-Time Chat
Week 3 (Days 15–21)
Day 15 — Flask-SocketIO Setup
Install and configure Flask-SocketIO. Redis as message broker. Basic connection/disconnection events. WebSocket authentication handshake using JWT. Test with two browser tabs. Time: 6hrs.
Day 16 — Chat Backend
Conversation creation logic. Message saving to database. SocketIO events: join_conversation, send_message, receive_message, typing_indicator. Rate limiting on messages. Time: 6hrs.
Day 17 — Chat UI
Chat page design. Conversation list sidebar, message thread view, input bar with emoji picker, typing indicator animation, timestamp display, read receipts UI. Time: 6hrs.
Day 18 — Song Sharing in Chat
Ability to share a song inside a chat message. Mini player card renders inside chat bubble. Clicking it opens full player. Backend handles song_id field in Messages table. Time: 6hrs.
Day 19 — Playlist Sharing in Chat
Same pattern as song sharing but for playlists. Playlist card renders inside chat with song count and cover collage. Time: 6hrs.
Day 20 — Voice Notes
Hold-to-record mic button in chat. MediaRecorder API in browser. Upload audio blob to Firebase Storage. Voice note URL saved to Messages. Playback UI inside chat bubble. Time: 6hrs.
Day 21 — Chat Polish + Notifications
Unread message badges. Real-time notification dot on nav. Message search. Scroll-to-bottom behavior. Mobile keyboard handling. Time: 6hrs.

PHASE 4 — Sync Engine (Hardest Week)
Week 4 (Days 22–28)
Day 22 — Sync Session Backend
API routes: create session, join session, end session. Session code generation. Sync_Sessions table logic. Host vs guest role assignment. Time: 6hrs.
Day 23 — WebSocket Sync Room
SocketIO room per sync session. Events: host_play, host_pause, host_seek, guest_join, sync_heartbeat. Server authoritative time broadcasting. Time: 6hrs.
Day 24 — Sync Engine Core (Drift Correction)
This is the hardest day. Latency ping measurement between client and server. Drift detection if client timestamp vs server timestamp differs by >300ms. Auto-realign algorithm that smoothly corrects position without jarring skip. Time: 6hrs.
Day 25 — Sync UI
Sync session page. Now playing with synced progress bar. Guest joined indicator. Connection quality indicator. Leave session button. Invite via session code UI. Time: 6hrs.
Day 26 — Real-Time Reactions
Emoji reaction buttons during sync playback. SocketIO broadcasts emoji + timestamp_position to all session members. Floating emoji animation rises from bottom of screen. Reactions saved to Reactions table. Time: 6hrs.
Day 27 — Voice Notes During Sync
Hold mic during sync session to record voice note attached to current timestamp. When other user reaches that timestamp, voice note plays over music. Complex but powerful feature. Time: 6hrs.
Day 28 — Sync Engine Testing + Fixes
Stress test the sync engine. Simulate bad network conditions. Fix drift edge cases. Test on mobile. Polish the UI. This day is purely QA and fixes. Time: 6hrs.

PHASE 5 — AI & Snap System
Week 5 (Days 29–35)
Day 29 — Snap Point Engine
Python functions for all snap transactions. +5 send song, +10 share playlist, +15 sync listen, +50 five consecutive syncs, +20 daily streak. Snap_Transactions table logic. Bond level calculation function. Time: 6hrs.
Day 30 — Snap Points UI
Snap points display on profile. Transaction history feed. Bond level progress bar with animation. Level-up notification popup. Time: 6hrs.
Day 31 — AI Compatibility Score
Python function that calculates Soul Sync Score. Genre overlap percentage, mood similarity score, listening time overlap, shared song frequency. Weighted formula produces 0–100 score. Saves to AI_Compatibility table. Time: 6hrs.
Day 32 — Compatibility UI
Compatibility page between two friends. Circular score display, breakdown bars per category, AI-generated explanation text, shared genres cloud, mood chart. Time: 6hrs.
Day 33 — AI Bond Analyzer
Weekly bond report generator. Python function analyzes interaction frequency, shared listening time, mood dominance, snap growth over 7 days. Generates summary paragraph. Saves to AI_Bond_Reports. Time: 6hrs.
Day 34 — Bond Report UI
Weekly bond report card UI. Bond growth percentage, emotional summary paragraph, dominant mood badge, suggestions section, share report button. Time: 6hrs.
Day 35 — Cron Job Setup
APScheduler in Flask to run bond analyzer every Sunday midnight. Test cron locally. Make sure it processes all active friend pairs. Time: 6hrs.

PHASE 6 — Mood Rooms & Gamification
Week 6 (Days 36–42)
Day 36 — Mood Rooms Backend
Predefined rooms seeded into database: Chill, Study, Gym, Party, Late Night Feels. Join/leave room API. Room members tracking. SocketIO room events for group sync. Time: 6hrs.
Day 37 — Mood Rooms UI
Rooms discovery page. Room cards with mood color coding, live member count, now playing song. Enter room button. Real-time presence dots. Time: 6hrs.
Day 38 — Group Chat in Mood Rooms
Group chat inside each mood room. SocketIO group messaging. Group snap bonus multiplier when chatting in rooms. Time: 6hrs.
Day 39 — Daily Challenges Backend
Daily_Challenges table seeded with challenges. User_Challenge_Progress tracking. API routes: get today's challenges, update progress, claim reward. Auto-reset at midnight. Time: 6hrs.
Day 40 — Daily Challenges UI
Challenges page. Challenge cards with progress bars, reward display, claim button animation, completed state. Streak protection mechanic UI. Time: 6hrs.
Day 41 — Memory Timeline Backend
Auto-record memory events. First sync together, first shared playlist, longest session, highest streak day. Memory_Timeline table population logic. Time: 6hrs.
Day 42 — Memory Timeline UI
Visual timeline page between two friends. Vertical timeline with event cards, song preview, date stamp, emotional label. Beautifully designed — this is an emotional feature. Time: 6hrs.

PHASE 7 — Polish, Security & Launch
Week 7 (Days 43–49)
Day 43 — Private Listening Mode
Private session flag in Sync_Sessions. No snap points awarded. No streak impact. Hidden from activity feed. Encrypted session indicator in UI. Time: 6hrs.
Day 44 — Security Hardening
Input sanitization everywhere. Rate limiting on all API routes. WebSocket auth verification on every event. SQL injection prevention audit. XSS prevention. Time: 6hrs.
Day 45 — Mobile Responsiveness Audit
Go through every single page on 320px, 375px, 768px, 1024px, 1440px, 4K. Fix every broken layout. Test bottom nav on mobile. Test touch interactions. Time: 6hrs.
Day 46 — Performance Optimization
Lazy loading images. CSS and JS minification. Database query optimization with proper indexes. Redis caching for frequently accessed data. Time: 6hrs.
Day 47 — Error Handling + Loading States
Every API call needs loading skeleton UI. Every error needs a proper user-facing message. Empty states for no friends, no songs, no messages. 404 page. Time: 6hrs.
Day 48 — Deployment
Deploy Flask backend to Render.com. Deploy frontend to Vercel. Set up environment variables. Connect Supabase PostgreSQL. Connect Upstash Redis. Domain setup. Time: 6hrs.
Day 49 — Final QA + Launch
Full end-to-end test as two different users. Fix any last bugs. Write basic README. Share your product. You're live. Time: 6hrs.
