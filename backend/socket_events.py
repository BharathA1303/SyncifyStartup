"""
WebSocket Event Handlers
========================
All Flask-SocketIO events registered here.
Imported by app.py at startup.
"""
from extensions import socketio
from flask_socketio import join_room, leave_room, emit, disconnect
from utils.auth_middleware import require_auth_ws
from utils.helpers import utcnow


# ============================================
# CONNECTION EVENTS
# ============================================

@socketio.on('connect')
def on_connect(auth):
    """Client connected — verify auth token."""
    user = require_auth_ws(auth)
    if not user:
        disconnect()
        return False
    emit('connected', {'status': 'ok', 'user_id': str(user.id)})


@socketio.on('disconnect')
def on_disconnect():
    """Client disconnected."""
    pass


# ============================================
# CHAT EVENTS
# ============================================

@socketio.on('join_conversation')
def on_join_conversation(data):
    """Join a private chat room."""
    user = require_auth_ws(data)
    if not user:
        return

    conversation_id = data.get('conversation_id')
    if conversation_id:
        join_room(f"conv_{conversation_id}")
        emit('joined_conversation', {'conversation_id': conversation_id})


@socketio.on('leave_conversation')
def on_leave_conversation(data):
    """Leave a chat room."""
    conversation_id = data.get('conversation_id')
    if conversation_id:
        leave_room(f"conv_{conversation_id}")


@socketio.on('typing')
def on_typing(data):
    """Broadcast typing indicator."""
    user = require_auth_ws(data)
    if not user:
        return
    conversation_id = data.get('conversation_id')
    if conversation_id:
        emit('user_typing', {
            'user_id': str(user.id),
            'username': user.username
        }, room=f"conv_{conversation_id}", include_self=False)


# ============================================
# SYNC SESSION EVENTS
# ============================================

@socketio.on('join_sync')
def on_join_sync(data):
    """Join a sync session room."""
    user = require_auth_ws(data)
    if not user:
        return

    session_code = data.get('session_code')
    if session_code:
        join_room(f"sync_{session_code}")
        emit('sync_joined', {
            'session_code': session_code,
            'user_id': str(user.id),
            'username': user.username
        }, room=f"sync_{session_code}")


@socketio.on('leave_sync')
def on_leave_sync(data):
    """Leave a sync session."""
    session_code = data.get('session_code')
    if session_code:
        leave_room(f"sync_{session_code}")


@socketio.on('sync_play')
def on_sync_play(data):
    """Host plays — broadcast to all in session."""
    user = require_auth_ws(data)
    if not user:
        return

    session_code = data.get('session_code')
    position = data.get('position', 0)
    server_time = utcnow().timestamp()

    emit('sync_play', {
        'position': position,
        'server_time': server_time,
        'triggered_by': str(user.id)
    }, room=f"sync_{session_code}", include_self=False)


@socketio.on('sync_pause')
def on_sync_pause(data):
    """Host pauses — broadcast to all in session."""
    user = require_auth_ws(data)
    if not user:
        return

    session_code = data.get('session_code')
    position = data.get('position', 0)

    emit('sync_pause', {
        'position': position,
        'triggered_by': str(user.id)
    }, room=f"sync_{session_code}", include_self=False)


@socketio.on('sync_seek')
def on_sync_seek(data):
    """Host seeks — broadcast new position."""
    user = require_auth_ws(data)
    if not user:
        return

    session_code = data.get('session_code')
    position = data.get('position', 0)
    server_time = utcnow().timestamp()

    emit('sync_seek', {
        'position': position,
        'server_time': server_time,
    }, room=f"sync_{session_code}", include_self=False)


@socketio.on('sync_heartbeat')
def on_sync_heartbeat(data):
    """
    Heartbeat for drift correction.
    Client sends current position, server replies with authoritative time.
    """
    session_code = data.get('session_code')
    client_position = data.get('position', 0)
    server_time = utcnow().timestamp()

    emit('sync_heartbeat_ack', {
        'server_time': server_time,
        'client_position': client_position,
    })


@socketio.on('sync_reaction')
def on_sync_reaction(data):
    """Broadcast emoji reaction to all in sync session."""
    user = require_auth_ws(data)
    if not user:
        return

    session_code = data.get('session_code')
    emoji = data.get('emoji', '❤️')
    position = data.get('position', 0)

    emit('sync_reaction', {
        'user_id': str(user.id),
        'username': user.username,
        'emoji': emoji,
        'position': position,
    }, room=f"sync_{session_code}")


# ============================================
# MOOD ROOM EVENTS
# ============================================

@socketio.on('join_room_event')
def on_join_mood_room(data):
    """Join a mood room."""
    user = require_auth_ws(data)
    if not user:
        return

    room_id = data.get('room_id')
    if room_id:
        join_room(f"room_{room_id}")
        emit('room_user_joined', {
            'user_id': str(user.id),
            'username': user.username,
            'profile_picture': user.profile_picture
        }, room=f"room_{room_id}")


@socketio.on('leave_room_event')
def on_leave_mood_room(data):
    """Leave a mood room."""
    user = require_auth_ws(data)
    if not user:
        return

    room_id = data.get('room_id')
    if room_id:
        leave_room(f"room_{room_id}")
        emit('room_user_left', {
            'user_id': str(user.id),
            'username': user.username
        }, room=f"room_{room_id}")