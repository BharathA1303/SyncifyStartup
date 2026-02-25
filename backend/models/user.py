"""
User Model
==========
SQLAlchemy ORM model for the users table.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow, calculate_bond_level
import uuid
from flask import Blueprint
users_bp = Blueprint('users', __name__)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    bio = db.Column(db.Text, default='')
    profile_picture = db.Column(db.Text, default='')
    snap_points = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_private = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    def to_dict(self, include_private=False):
        """Serialize user to dictionary."""
        data = {
            'id': self.id,
            'username': self.username,
            'bio': self.bio,
            'profile_picture': self.profile_picture,
            'snap_points': self.snap_points,
            'bond_level': calculate_bond_level(self.snap_points),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_private:
            data.update({
                'email': self.email,
                'is_private': self.is_private,
                'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            })
        return data

    def to_public_dict(self):
        """Minimal public profile."""
        return {
            'id': self.id,
            'username': self.username,
            'profile_picture': self.profile_picture,
            'snap_points': self.snap_points,
            'bond_level': calculate_bond_level(self.snap_points),
        }

    def add_snap_points(self, points):
        """Add snap points to user."""
        self.snap_points = (self.snap_points or 0) + points
        db.session.commit()

    @staticmethod
    def get_by_firebase_uid(uid):
        return User.query.filter_by(firebase_uid=uid).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return f'<User {self.username}>'