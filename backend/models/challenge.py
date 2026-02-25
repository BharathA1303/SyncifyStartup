"""
Challenge Models
================
Daily challenges and user progress tracking.
"""
from extensions import db
from utils.helpers import generate_uuid, utcnow
from datetime import date


class DailyChallenge(db.Model):
    __tablename__ = 'daily_challenges'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    challenge_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_count = db.Column(db.Integer, default=1)
    reward_points = db.Column(db.Integer, nullable=False)
    reward_type = db.Column(db.String(30), default='snap_points')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    def to_dict(self, user_progress=None):
        data = {
            'id': self.id,
            'challenge_type': self.challenge_type,
            'title': self.title,
            'description': self.description,
            'target_count': self.target_count,
            'reward_points': self.reward_points,
            'reward_type': self.reward_type,
        }
        if user_progress:
            data['progress'] = {
                'count': user_progress.progress_count,
                'completed': user_progress.completed,
                'percentage': min(100, int((user_progress.progress_count / self.target_count) * 100)),
            }
        else:
            data['progress'] = {'count': 0, 'completed': False, 'percentage': 0}
        return data


class UserChallengeProgress(db.Model):
    __tablename__ = 'user_challenge_progress'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    challenge_id = db.Column(db.String(36), db.ForeignKey('daily_challenges.id', ondelete='CASCADE'), nullable=False)
    progress_count = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime(timezone=True))
    date = db.Column(db.Date, default=date.today)

    challenge = db.relationship('DailyChallenge', foreign_keys=[challenge_id])
    user = db.relationship('User', foreign_keys=[user_id])

    def complete(self):
        self.completed = True
        self.completed_at = utcnow()
        db.session.commit()