"""
Flask extensions — initialized here, imported everywhere.
This pattern avoids circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_migrate import Migrate
import redis
import os

# Database ORM
db = SQLAlchemy()

# Real-time WebSocket engine
socketio = SocketIO()

# API rate limiter
limiter = Limiter(key_func=get_remote_address)

# Cross-origin resource sharing
cors = CORS()

# Database migration manager
migrate = Migrate()

# Redis client (initialized in app factory)
redis_client = None

def init_redis(app):
    """Initialize Redis connection."""
    global redis_client
    redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
    redis_client = redis.from_url(redis_url, decode_responses=True)
    return redis_client

def get_redis():
    """Get the Redis client instance."""
    return redis_client