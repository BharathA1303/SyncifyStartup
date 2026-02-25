"""
Playlist Model
==============
User-created playlists with songs.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    cover_image = db.Column(db.Text, default='')
    is_public = db.Column(db.Boolean, default=False)
    song_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    owner = db.relationship('User', foreign_keys=[user_id], backref='playlists')
    playlist_songs = db.relationship('PlaylistSong', backref='playlist', cascade='all, delete-orphan')

    def to_dict(self, include_songs=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'cover_image': self.cover_image,
            'is_public': self.is_public,
            'song_count': self.song_count,
            'owner': self.owner.to_public_dict() if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_songs:
            data['songs'] = [
                ps.song.to_dict() for ps in
                sorted(self.playlist_songs, key=lambda x: x.position)
                if ps.song
            ]
        return data

    def to_mini_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cover_image': self.cover_image,
            'song_count': self.song_count,
            'owner': self.owner.to_public_dict() if self.owner else None,
        }

    def __repr__(self):
        return f'<Playlist {self.name}>'


class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    playlist_id = db.Column(db.String(36), db.ForeignKey('playlists.id', ondelete='CASCADE'), nullable=False)
    song_id = db.Column(db.String(36), db.ForeignKey('songs.id', ondelete='CASCADE'), nullable=False)
    position = db.Column(db.Integer, default=0)
    added_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    # Relationships
    song = db.relationship('Song', backref='playlist_entries')

    def __repr__(self):
        return f'<PlaylistSong playlist={self.playlist_id} song={self.song_id}>'