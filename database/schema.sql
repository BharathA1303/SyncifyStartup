-- ============================================
-- SYNCIFY DATABASE SCHEMA
-- PostgreSQL — Full Production Schema
-- Run: psql -U postgres -d syncify_db -f schema.sql
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    firebase_uid VARCHAR(128) UNIQUE NOT NULL,
    username VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    bio TEXT DEFAULT '',
    profile_picture TEXT DEFAULT '',
    snap_points INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    is_private BOOLEAN DEFAULT FALSE,
    last_seen TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_firebase_uid ON users(firebase_uid);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- ============================================
-- FRIENDSHIPS
-- ============================================
CREATE TABLE IF NOT EXISTS friendships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    requester_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'blocked')),
    streak_count INTEGER DEFAULT 0,
    last_interaction_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(requester_id, receiver_id),
    CHECK (requester_id != receiver_id)
);

CREATE INDEX idx_friendships_requester ON friendships(requester_id);
CREATE INDEX idx_friendships_receiver ON friendships(receiver_id);
CREATE INDEX idx_friendships_status ON friendships(status);

-- ============================================
-- SONGS
-- ============================================
CREATE TABLE IF NOT EXISTS songs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    uploaded_by UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    album VARCHAR(255) DEFAULT '',
    genre VARCHAR(50) NOT NULL,
    mood_tag VARCHAR(50) NOT NULL,
    duration INTEGER NOT NULL, -- seconds
    file_url TEXT NOT NULL,
    cover_image TEXT DEFAULT '',
    play_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_songs_genre ON songs(genre);
CREATE INDEX idx_songs_mood_tag ON songs(mood_tag);
CREATE INDEX idx_songs_uploaded_by ON songs(uploaded_by);

-- ============================================
-- PLAYLISTS
-- ============================================
CREATE TABLE IF NOT EXISTS playlists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    cover_image TEXT DEFAULT '',
    is_public BOOLEAN DEFAULT FALSE,
    song_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_playlists_user_id ON playlists(user_id);
CREATE INDEX idx_playlists_is_public ON playlists(is_public);

-- ============================================
-- PLAYLIST SONGS (Join Table)
-- ============================================
CREATE TABLE IF NOT EXISTS playlist_songs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    playlist_id UUID NOT NULL REFERENCES playlists(id) ON DELETE CASCADE,
    song_id UUID NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
    position INTEGER DEFAULT 0,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(playlist_id, song_id)
);

CREATE INDEX idx_playlist_songs_playlist ON playlist_songs(playlist_id);
CREATE INDEX idx_playlist_songs_song ON playlist_songs(song_id);

-- ============================================
-- CONVERSATIONS
-- ============================================
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user1_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    last_message_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user1_id, user2_id),
    CHECK (user1_id != user2_id)
);

CREATE INDEX idx_conversations_user1 ON conversations(user1_id);
CREATE INDEX idx_conversations_user2 ON conversations(user2_id);
CREATE INDEX idx_conversations_last_message ON conversations(last_message_at DESC);

-- ============================================
-- MESSAGES
-- ============================================
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text TEXT DEFAULT '',
    song_id UUID REFERENCES songs(id) ON DELETE SET NULL,
    playlist_id UUID REFERENCES playlists(id) ON DELETE SET NULL,
    voice_note_url TEXT DEFAULT '',
    message_type VARCHAR(20) DEFAULT 'text' CHECK (message_type IN ('text', 'song', 'playlist', 'voice_note')),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);

-- ============================================
-- SYNC SESSIONS
-- ============================================
CREATE TABLE IF NOT EXISTS sync_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_code VARCHAR(20) UNIQUE NOT NULL,
    host_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    guest_id UUID REFERENCES users(id) ON DELETE SET NULL,
    song_id UUID REFERENCES songs(id) ON DELETE SET NULL,
    current_position FLOAT DEFAULT 0, -- seconds
    is_playing BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_sync_sessions_code ON sync_sessions(session_code);
CREATE INDEX idx_sync_sessions_host ON sync_sessions(host_id);
CREATE INDEX idx_sync_sessions_active ON sync_sessions(is_active);

-- ============================================
-- REACTIONS (During Sync)
-- ============================================
CREATE TABLE IF NOT EXISTS reactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sync_session_id UUID NOT NULL REFERENCES sync_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    timestamp_position FLOAT NOT NULL, -- position in song (seconds)
    emoji VARCHAR(10) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_reactions_session ON reactions(sync_session_id);
CREATE INDEX idx_reactions_user ON reactions(user_id);

-- ============================================
-- SNAP TRANSACTIONS
-- ============================================
CREATE TABLE IF NOT EXISTS snap_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user1_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID REFERENCES users(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,
    points_added INTEGER NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_snap_transactions_user1 ON snap_transactions(user1_id);
CREATE INDEX idx_snap_transactions_action ON snap_transactions(action_type);
CREATE INDEX idx_snap_transactions_created ON snap_transactions(created_at DESC);

-- ============================================
-- AI COMPATIBILITY
-- ============================================
CREATE TABLE IF NOT EXISTS ai_compatibility (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user1_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    compatibility_score FLOAT DEFAULT 0,
    genre_overlap_score FLOAT DEFAULT 0,
    mood_similarity_score FLOAT DEFAULT 0,
    listening_overlap_score FLOAT DEFAULT 0,
    shared_songs_score FLOAT DEFAULT 0,
    shared_genres JSONB DEFAULT '[]',
    shared_moods JSONB DEFAULT '[]',
    ai_explanation TEXT DEFAULT '',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user1_id, user2_id)
);

CREATE INDEX idx_ai_compat_users ON ai_compatibility(user1_id, user2_id);

-- ============================================
-- AI BOND REPORTS
-- ============================================
CREATE TABLE IF NOT EXISTS ai_bond_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user1_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    weekly_summary_text TEXT DEFAULT '',
    bond_growth_percentage FLOAT DEFAULT 0,
    dominant_mood VARCHAR(50) DEFAULT '',
    sync_sessions_count INTEGER DEFAULT 0,
    messages_count INTEGER DEFAULT 0,
    songs_shared_count INTEGER DEFAULT 0,
    suggestions JSONB DEFAULT '[]',
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bond_reports_users ON ai_bond_reports(user1_id, user2_id);
CREATE INDEX idx_bond_reports_generated ON ai_bond_reports(generated_at DESC);

-- ============================================
-- MOOD ROOMS
-- ============================================
CREATE TABLE IF NOT EXISTS mood_rooms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    mood_type VARCHAR(50) NOT NULL,
    description TEXT DEFAULT '',
    cover_image TEXT DEFAULT '',
    current_song_id UUID REFERENCES songs(id) ON DELETE SET NULL,
    is_public BOOLEAN DEFAULT TRUE,
    snap_multiplier FLOAT DEFAULT 1.5,
    member_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- MOOD ROOM MEMBERS
-- ============================================
CREATE TABLE IF NOT EXISTS mood_room_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    room_id UUID NOT NULL REFERENCES mood_rooms(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(room_id, user_id)
);

CREATE INDEX idx_room_members_room ON mood_room_members(room_id);
CREATE INDEX idx_room_members_user ON mood_room_members(user_id);

-- ============================================
-- DAILY CHALLENGES
-- ============================================
CREATE TABLE IF NOT EXISTS daily_challenges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    challenge_type VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    target_count INTEGER DEFAULT 1,
    reward_points INTEGER NOT NULL,
    reward_type VARCHAR(30) DEFAULT 'snap_points' CHECK (reward_type IN ('snap_points', 'streak_shield', 'multiplier')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- USER CHALLENGE PROGRESS
-- ============================================
CREATE TABLE IF NOT EXISTS user_challenge_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    challenge_id UUID NOT NULL REFERENCES daily_challenges(id) ON DELETE CASCADE,
    progress_count INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    date DATE DEFAULT CURRENT_DATE,
    UNIQUE(user_id, challenge_id, date)
);

CREATE INDEX idx_challenge_progress_user ON user_challenge_progress(user_id);
CREATE INDEX idx_challenge_progress_date ON user_challenge_progress(date);

-- ============================================
-- MEMORY TIMELINE
-- ============================================
CREATE TABLE IF NOT EXISTS memory_timeline (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user1_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN (
        'first_sync', 'first_playlist_shared', 'first_message',
        'longest_sync', 'highest_streak', 'first_song_shared',
        'level_up', 'milestone'
    )),
    song_id UUID REFERENCES songs(id) ON DELETE SET NULL,
    playlist_id UUID REFERENCES playlists(id) ON DELETE SET NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_memory_timeline_users ON memory_timeline(user1_id, user2_id);
CREATE INDEX idx_memory_timeline_created ON memory_timeline(created_at DESC);

-- ============================================
-- TRIGGER: Auto-update updated_at timestamps
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_friendships_updated_at
    BEFORE UPDATE ON friendships
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_playlists_updated_at
    BEFORE UPDATE ON playlists
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================
-- SEED: Default Mood Rooms
-- ============================================
INSERT INTO mood_rooms (name, mood_type, description, snap_multiplier) VALUES
('Chill Zone', 'chill', 'Laid back vibes. Come unwind.', 1.5),
('Study Hours', 'study', 'Focus mode. No distractions.', 1.3),
('Gym Energy', 'gym', 'Get pumped. Lift heavy.', 1.8),
('Party Mode', 'party', 'Turn it up. Dance all night.', 2.0),
('Late Night Feels', 'late_night', 'It''s 3AM and you''re still awake.', 1.5)
ON CONFLICT DO NOTHING;

-- ============================================
-- SEED: Daily Challenges
-- ============================================
INSERT INTO daily_challenges (challenge_type, title, description, target_count, reward_points, reward_type) VALUES
('share_song', 'Music Messenger', 'Share 2 songs with friends today', 2, 20, 'snap_points'),
('sync_listen', 'In Sync', 'Do 1 sync listen session today', 1, 30, 'snap_points'),
('create_playlist', 'Playlist Creator', 'Create or update a shared playlist', 1, 25, 'snap_points'),
('send_message', 'Keep Talking', 'Send 10 messages today', 10, 15, 'snap_points'),
('join_room', 'Room Explorer', 'Join a mood room today', 1, 20, 'snap_points'),
('react_sync', 'Emoji Reactor', 'Drop 5 reactions during sync sessions', 5, 15, 'snap_points'),
('consecutive_sync', 'Streak Guardian', 'Complete a sync session 3 days in a row', 3, 50, 'streak_shield')
ON CONFLICT DO NOTHING;