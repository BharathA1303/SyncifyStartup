"""
Song Model
==========
Represents an audio track in the system.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow, format_duration


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    uploaded_by = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), default='')
    genre = db.Column(db.String(50), nullable=False)
    mood_tag = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # seconds
    file_url = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.Text, default='')
    play_count = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    # Relationships
    uploader = db.relationship('User', foreign_keys=[uploaded_by], backref='uploaded_songs')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'genre': self.genre,
            'mood_tag': self.mood_tag,
            'duration': self.duration,
            'duration_formatted': format_duration(self.duration),
            'file_url': self.file_url,
            'cover_image': self.cover_image,
            'play_count': self.play_count,
            'is_public': self.is_public,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def to_mini_dict(self):
        """Minimal song info for embedding in messages/chat."""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'cover_image': self.cover_image,
            'duration': self.duration,
            'duration_formatted': format_duration(self.duration),
        }

    def increment_play_count(self):
        self.play_count = (self.play_count or 0) + 1
        db.session.commit()

    def __repr__(self):
        return f'<Song {self.title} by {self.artist}>'