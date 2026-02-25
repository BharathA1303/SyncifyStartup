"""
AI Models
=========
Compatibility scores and weekly bond reports.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow


class AICompatibility(db.Model):
    __tablename__ = 'ai_compatibility'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user1_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    compatibility_score = db.Column(db.Float, default=0.0)
    genre_overlap_score = db.Column(db.Float, default=0.0)
    mood_similarity_score = db.Column(db.Float, default=0.0)
    listening_overlap_score = db.Column(db.Float, default=0.0)
    shared_songs_score = db.Column(db.Float, default=0.0)
    shared_genres = db.Column(db.JSON, default=list)
    shared_moods = db.Column(db.JSON, default=list)
    ai_explanation = db.Column(db.Text, default='')
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])

    def to_dict(self):
        return {
            'id': self.id,
            'compatibility_score': round(self.compatibility_score, 1),
            'breakdown': {
                'genre_overlap': round(self.genre_overlap_score, 1),
                'mood_similarity': round(self.mood_similarity_score, 1),
                'listening_overlap': round(self.listening_overlap_score, 1),
                'shared_songs': round(self.shared_songs_score, 1),
            },
            'shared_genres': self.shared_genres or [],
            'shared_moods': self.shared_moods or [],
            'ai_explanation': self.ai_explanation,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def get_or_create(user1_id, user2_id):
        uid1, uid2 = sorted([str(user1_id), str(user2_id)])
        compat = AICompatibility.query.filter_by(user1_id=uid1, user2_id=uid2).first()
        if not compat:
            compat = AICompatibility(user1_id=uid1, user2_id=uid2)
            db.session.add(compat)
            db.session.commit()
        return compat


class AIBondReport(db.Model):
    __tablename__ = 'ai_bond_reports'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user1_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    weekly_summary_text = db.Column(db.Text, default='')
    bond_growth_percentage = db.Column(db.Float, default=0.0)
    dominant_mood = db.Column(db.String(50), default='')
    sync_sessions_count = db.Column(db.Integer, default=0)
    messages_count = db.Column(db.Integer, default=0)
    songs_shared_count = db.Column(db.Integer, default=0)
    suggestions = db.Column(db.JSON, default=list)
    generated_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'weekly_summary_text': self.weekly_summary_text,
            'bond_growth_percentage': round(self.bond_growth_percentage, 1),
            'dominant_mood': self.dominant_mood,
            'stats': {
                'sync_sessions': self.sync_sessions_count,
                'messages': self.messages_count,
                'songs_shared': self.songs_shared_count,
            },
            'suggestions': self.suggestions or [],
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
        }


class MemoryTimeline(db.Model):
    __tablename__ = 'memory_timeline'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user1_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    song_id = db.Column(db.String(36), db.ForeignKey('songs.id', ondelete='SET NULL'), nullable=True)
    playlist_id = db.Column(db.String(36), db.ForeignKey('playlists.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    extra_data = db.Column(db.JSON, default=dict)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    song = db.relationship('Song', foreign_keys=[song_id])
    playlist = db.relationship('Playlist', foreign_keys=[playlist_id])

    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'title': self.title,
            'description': self.description,
            'song': self.song.to_mini_dict() if self.song else None,
            'playlist': self.playlist.to_mini_dict() if self.playlist else None,
            'extra_data': self.extra_data or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def record(user1_id, user2_id, event_type, title, description='', **kwargs):
        """Convenience method to record a memory event."""
        uid1, uid2 = sorted([str(user1_id), str(user2_id)])
        event = MemoryTimeline(
            user1_id=uid1,
            user2_id=uid2,
            event_type=event_type,
            title=title,
            description=description,
            song_id=kwargs.get('song_id'),
            playlist_id=kwargs.get('playlist_id'),
            extra_data=kwargs.get('extra_data', {}),
        )
        db.session.add(event)
        db.session.commit()
        return event