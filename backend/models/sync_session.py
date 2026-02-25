"""
Sync Session Model
==================
Real-time synchronized listening sessions.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow, generate_session_code


class SyncSession(db.Model):
    __tablename__ = 'sync_sessions'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    session_code = db.Column(db.String(20), unique=True, nullable=False, default=generate_session_code)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    song_id = db.Column(db.String(36), db.ForeignKey('songs.id', ondelete='SET NULL'), nullable=True)
    current_position = db.Column(db.Float, default=0.0)
    is_playing = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    started_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    ended_at = db.Column(db.DateTime(timezone=True))

    # Relationships
    host = db.relationship('User', foreign_keys=[host_id], backref='hosted_sessions')
    guest = db.relationship('User', foreign_keys=[guest_id], backref='joined_sessions')
    song = db.relationship('Song', foreign_keys=[song_id])
    reactions = db.relationship('Reaction', backref='session', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'session_code': self.session_code,
            'host': self.host.to_public_dict() if self.host else None,
            'guest': self.guest.to_public_dict() if self.guest else None,
            'song': self.song.to_dict() if self.song else None,
            'current_position': self.current_position,
            'is_playing': self.is_playing,
            'is_private': self.is_private,
            'is_active': self.is_active,
            'started_at': self.started_at.isoformat() if self.started_at else None,
        }

    def end_session(self):
        self.is_active = False
        self.ended_at = utcnow()
        db.session.commit()

    def duration_seconds(self):
        """Total session duration in seconds."""
        if not self.started_at:
            return 0
        end = self.ended_at or utcnow()
        return (end - self.started_at).total_seconds()

    def __repr__(self):
        return f'<SyncSession {self.session_code}>'


class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    sync_session_id = db.Column(db.String(36), db.ForeignKey('sync_sessions.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    timestamp_position = db.Column(db.Float, nullable=False)
    emoji = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    user = db.relationship('User', foreign_keys=[user_id])

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'timestamp_position': self.timestamp_position,
            'emoji': self.emoji,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }