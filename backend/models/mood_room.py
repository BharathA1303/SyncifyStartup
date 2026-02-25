"""
Mood Room Model
===============
Public mood-based listening rooms.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow


class MoodRoom(db.Model):
    __tablename__ = 'mood_rooms'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    mood_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, default='')
    cover_image = db.Column(db.Text, default='')
    current_song_id = db.Column(db.String(36), db.ForeignKey('songs.id', ondelete='SET NULL'), nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    snap_multiplier = db.Column(db.Float, default=1.5)
    member_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    current_song = db.relationship('Song', foreign_keys=[current_song_id])
    members = db.relationship('MoodRoomMember', backref='room', cascade='all, delete-orphan')

    # Mood gradient map for UI
    MOOD_GRADIENTS = {
        'chill':       'linear-gradient(135deg, #2cb67d, #7f5af0)',
        'study':       'linear-gradient(135deg, #3a86ff, #8338ec)',
        'gym':         'linear-gradient(135deg, #ff006e, #fb5607)',
        'party':       'linear-gradient(135deg, #ffbe0b, #fb5607)',
        'late_night':  'linear-gradient(135deg, #0d0221, #7f5af0)',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mood_type': self.mood_type,
            'description': self.description,
            'cover_image': self.cover_image,
            'current_song': self.current_song.to_mini_dict() if self.current_song else None,
            'is_public': self.is_public,
            'snap_multiplier': self.snap_multiplier,
            'member_count': self.member_count,
            'gradient': self.MOOD_GRADIENTS.get(self.mood_type, 'linear-gradient(135deg, #7f5af0, #2cb67d)'),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<MoodRoom {self.name}>'


class MoodRoomMember(db.Model):
    __tablename__ = 'mood_room_members'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    room_id = db.Column(db.String(36), db.ForeignKey('mood_rooms.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    joined_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    user = db.relationship('User', foreign_keys=[user_id])