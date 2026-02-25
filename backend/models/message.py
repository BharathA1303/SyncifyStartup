"""
Message & Conversation Models
==============================
Real-time chat between users.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user1_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    last_message_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    # Relationships
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    messages = db.relationship('Message', backref='conversation',
                                cascade='all, delete-orphan',
                                order_by='Message.created_at')

    def to_dict(self, current_user_id=None):
        other_user = None
        if current_user_id:
            other_user = self.user2 if str(self.user1_id) == str(current_user_id) else self.user1
        return {
            'id': self.id,
            'other_user': other_user.to_public_dict() if other_user else None,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def get_or_create(user1_id, user2_id):
        """Get existing conversation or create new one."""
        # Ensure consistent ordering
        uid1, uid2 = sorted([str(user1_id), str(user2_id)])
        conv = Conversation.query.filter(
            db.or_(
                db.and_(Conversation.user1_id == uid1, Conversation.user2_id == uid2),
                db.and_(Conversation.user1_id == uid2, Conversation.user2_id == uid1),
            )
        ).first()
        if not conv:
            conv = Conversation(user1_id=uid1, user2_id=uid2)
            db.session.add(conv)
            db.session.commit()
        return conv

    def __repr__(self):
        return f'<Conversation {self.user1_id} <-> {self.user2_id}>'


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.Text, default='')
    song_id = db.Column(db.String(36), db.ForeignKey('songs.id', ondelete='SET NULL'), nullable=True)
    playlist_id = db.Column(db.String(36), db.ForeignKey('playlists.id', ondelete='SET NULL'), nullable=True)
    voice_note_url = db.Column(db.Text, default='')
    message_type = db.Column(db.String(20), default='text')  # text, song, playlist, voice_note
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id])
    song = db.relationship('Song', foreign_keys=[song_id])
    playlist = db.relationship('Playlist', foreign_keys=[playlist_id])

    def to_dict(self):
        data = {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'sender': self.sender.to_public_dict() if self.sender else None,
            'text': self.text,
            'message_type': self.message_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if self.song:
            data['song'] = self.song.to_mini_dict()
        if self.playlist:
            data['playlist'] = self.playlist.to_mini_dict()
        if self.voice_note_url:
            data['voice_note_url'] = self.voice_note_url
        return data

    def __repr__(self):
        return f'<Message {self.id} type={self.message_type}>'