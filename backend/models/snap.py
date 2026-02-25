"""
Snap Transaction Model
======================
Tracks all snap point awards and history.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow


class SnapTransaction(db.Model):
    __tablename__ = 'snap_transactions'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user1_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    action_type = db.Column(db.String(50), nullable=False)
    points_added = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])

    # Action type constants
    ACTION_SEND_SONG = 'send_song'             # +5
    ACTION_SHARE_PLAYLIST = 'share_playlist'   # +10
    ACTION_SYNC_LISTEN = 'sync_listen'         # +15
    ACTION_CONSECUTIVE_SYNC = 'consecutive_sync'  # +50
    ACTION_DAILY_STREAK = 'daily_streak'       # +20
    ACTION_CHALLENGE = 'challenge_complete'    # varies
    ACTION_ROOM_BONUS = 'room_bonus'           # multiplier

    POINT_VALUES = {
        ACTION_SEND_SONG: 5,
        ACTION_SHARE_PLAYLIST: 10,
        ACTION_SYNC_LISTEN: 15,
        ACTION_CONSECUTIVE_SYNC: 50,
        ACTION_DAILY_STREAK: 20,
    }

    def to_dict(self):
        return {
            'id': self.id,
            'action_type': self.action_type,
            'points_added': self.points_added,
            'description': self.description,
            'user2': self.user2.to_public_dict() if self.user2 else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<SnapTransaction {self.action_type} +{self.points_added}>'