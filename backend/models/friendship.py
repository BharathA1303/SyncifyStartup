"""
Friendship Model
================
Handles friend requests, acceptance, streaks.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow


class Friendship(db.Model):
    __tablename__ = 'friendships'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    requester_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, blocked
    streak_count = db.Column(db.Integer, default=0)
    last_interaction_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    requester = db.relationship('User', foreign_keys=[requester_id], backref='sent_requests')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_requests')

    def to_dict(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'receiver_id': self.receiver_id,
            'status': self.status,
            'streak_count': self.streak_count,
            'last_interaction_date': self.last_interaction_date.isoformat() if self.last_interaction_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def to_dict_with_user(self, current_user_id):
        """Return friendship with the other user's profile."""
        other_user = self.receiver if str(self.requester_id) == str(current_user_id) else self.requester
        return {
            **self.to_dict(),
            'user': other_user.to_public_dict() if other_user else None,
        }

    @staticmethod
    def get_friendship(user1_id, user2_id):
        """Get friendship between two users regardless of who requested."""
        return Friendship.query.filter(
            db.or_(
                db.and_(Friendship.requester_id == user1_id, Friendship.receiver_id == user2_id),
                db.and_(Friendship.requester_id == user2_id, Friendship.receiver_id == user1_id)
            )
        ).first()

    @staticmethod
    def are_friends(user1_id, user2_id):
        """Check if two users are friends."""
        f = Friendship.get_friendship(user1_id, user2_id)
        return f is not None and f.status == 'accepted'

    def __repr__(self):
        return f'<Friendship {self.requester_id} -> {self.receiver_id} [{self.status}]>'