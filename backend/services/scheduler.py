"""
Scheduler Service
=================
APScheduler cron jobs.
- Weekly bond reports (every Sunday midnight)
- Daily challenge reset (every midnight)
- Streak checks (every midnight)
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def start_scheduler(app):
    """Initialize and start the background scheduler."""
    with app.app_context():

        # Weekly bond report — every Sunday at midnight
        scheduler.add_job(
            func=lambda: _run_with_context(app, generate_weekly_bond_reports),
            trigger=CronTrigger(day_of_week='sun', hour=0, minute=0),
            id='weekly_bond_reports',
            replace_existing=True
        )

        # Daily challenge reset — every day at midnight
        scheduler.add_job(
            func=lambda: _run_with_context(app, reset_daily_challenges),
            trigger=CronTrigger(hour=0, minute=0),
            id='daily_challenge_reset',
            replace_existing=True
        )

        # Streak check — every day at 11:59pm
        scheduler.add_job(
            func=lambda: _run_with_context(app, check_streaks),
            trigger=CronTrigger(hour=23, minute=59),
            id='streak_check',
            replace_existing=True
        )

    scheduler.start()
    logger.info("✅ Scheduler started with 3 jobs")


def _run_with_context(app, func):
    """Run a function inside Flask app context."""
    with app.app_context():
        try:
            func()
        except Exception as e:
            logger.error(f"Scheduler job failed [{func.__name__}]: {e}")


def generate_weekly_bond_reports():
    """Generate AI bond reports for all active friendships."""
    from models.friendship import Friendship
    from services.ai_service import generate_bond_report

    friendships = Friendship.query.filter_by(status='accepted').all()
    count = 0
    for f in friendships:
        try:
            generate_bond_report(str(f.requester_id), str(f.receiver_id))
            count += 1
        except Exception as e:
            logger.warning(f"Bond report failed for {f.id}: {e}")

    logger.info(f"Generated {count} bond reports")


def reset_daily_challenges():
    """Daily challenges auto-reset — progress tracked per date, so this is a no-op."""
    logger.info("Daily challenges reset (date-based, auto-resets)")


def check_streaks():
    """Check for broken streaks and notify users."""
    from models.friendship import Friendship
    from extensions import db
    from datetime import date, timedelta

    yesterday = date.today() - timedelta(days=1)
    friendships = Friendship.query.filter_by(status='accepted').all()

    broken = 0
    for f in friendships:
        if f.last_interaction_date and f.last_interaction_date < yesterday:
            if f.streak_count > 0:
                f.streak_count = 0
                broken += 1

    if broken:
        db.session.commit()
        logger.info(f"Reset {broken} broken streaks")