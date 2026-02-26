"""
SYNCIFY Backend — Flask Application Factory
==========================================
Production-ready Flask app with SocketIO, PostgreSQL, Redis.
"""
import eventlet
eventlet.monkey_patch()

import os
from flask import send_from_directory
from flask import Flask, jsonify
from config.settings import get_config
from extensions import db, socketio, limiter, cors, migrate, init_redis

# Import all models so SQLAlchemy registers them
import models  # noqa: F401

# Import all Socket event handlers
import socket_events  # noqa: F401

app = Flask(__name__)


def create_app(config=None):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load config
    app.config.from_object(config or get_config())

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {"origins": app.config.get('CORS_ORIGINS', ['*'])}
    })
    socketio.init_app(
        app,
        cors_allowed_origins=app.config.get('SOCKETIO_CORS_ALLOWED_ORIGINS', '*'),
        async_mode=app.config.get('SOCKETIO_ASYNC_MODE', 'eventlet'),
        message_queue=app.config.get('REDIS_URL'),
        logger=app.config.get('DEBUG', False),
        engineio_logger=False,
    )

    # Initialize Redis
    init_redis(app)

    # Register blueprints (API routes)
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Initialize Firebase
    init_firebase(app)

    # Initialize scheduler (cron jobs)
    if not app.config.get('TESTING'):
        init_scheduler(app)

    return app


def register_blueprints(app):
    """Register all API route blueprints."""
    from api.auth import auth_bp
    from api.users import users_bp
    from api.songs import songs_bp
    from api.playlists import playlists_bp
    from api.messages import messages_bp
    from api.sync import sync_bp
    from api.snaps import snaps_bp
    from api.rooms import rooms_bp
    from api.challenges import challenges_bp
    from api.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(songs_bp, url_prefix='/api/songs')
    app.register_blueprint(playlists_bp, url_prefix='/api/playlists')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(sync_bp, url_prefix='/api/sync')
    app.register_blueprint(snaps_bp, url_prefix='/api/snaps')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    app.register_blueprint(challenges_bp, url_prefix='/api/challenges')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')


def register_error_handlers(app):
    """Register global error handlers."""

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404

    @app.errorhandler(429)
    def rate_limited(e):
        return jsonify({'error': 'Rate limited', 'message': 'Too many requests'}), 429

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Server error', 'message': 'Internal server error'}), 500

    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'ok', 'service': 'syncify-api'}), 200
    # ============================================
    # Static File Serving (Development)
    # ============================================
    import os as _os

    @app.route('/')
    def serve_index():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'index.html')

    @app.route('/login')
    @app.route('/login.html')
    def serve_login():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'login.html')

    @app.route('/signup')
    @app.route('/signup.html')
    def serve_signup():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'signup.html')

    @app.route('/dashboard')
    @app.route('/dashboard.html')
    def serve_dashboard():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'dashboard.html')

    @app.route('/profile')
    @app.route('/profile.html')
    def serve_profile():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'profile.html')

    @app.route('/friends')
    @app.route('/friends.html')
    def serve_friends():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'friends.html')

    @app.route('/chat')
    @app.route('/chat.html')
    def serve_chat():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'chat.html')

    @app.route('/sync')
    @app.route('/sync.html')
    def serve_sync():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'sync.html')

    @app.route('/rooms')
    @app.route('/rooms.html')
    def serve_rooms():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'rooms.html')

    @app.route('/playlists')
    @app.route('/playlists.html')
    def serve_playlists():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'playlists.html')

    @app.route('/challenges')
    @app.route('/challenges.html')
    def serve_challenges():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'challenges.html')

    @app.route('/timeline')
    @app.route('/timeline.html')
    def serve_timeline():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'timeline.html')

    @app.route('/compatibility')
    @app.route('/compatibility.html')
    def serve_compatibility():
        pages_dir = _os.path.join(
            _os.path.dirname(_os.path.dirname(__file__)),
            'frontend', 'pages'
        )
        return send_from_directory(pages_dir, 'compatibility.html')


def init_firebase(app):
    """Initialize Firebase Admin SDK."""
    try:
        import firebase_admin
        from firebase_admin import credentials
        import json

        cred_dict = {
            "type": "service_account",
            "project_id": app.config.get('FIREBASE_PROJECT_ID'),
            "private_key_id": app.config.get('FIREBASE_PRIVATE_KEY_ID', ''),
            "private_key": app.config.get('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
            "client_email": app.config.get('FIREBASE_CLIENT_EMAIL', ''),
            "client_id": app.config.get('FIREBASE_CLIENT_ID', ''),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }

        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'storageBucket': app.config.get('FIREBASE_STORAGE_BUCKET')
            })
        app.logger.info("✅ Firebase initialized")
    except Exception as e:
        app.logger.warning(f"⚠️  Firebase not configured: {e}")


def init_scheduler(app):
    """Initialize APScheduler for cron jobs."""
    try:
        from services.scheduler import start_scheduler
        start_scheduler(app)
        app.logger.info("✅ Scheduler initialized")
    except Exception as e:
        app.logger.warning(f"⚠️  Scheduler not started: {e}")

# ============================================
# Static File Serving (Development)
# ============================================
import os as _os

@app.route('/')
def serve_index():
    pages_dir = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'pages')
    return send_from_directory(pages_dir, 'index.html')

@app.route('/login')
def serve_login():
    pages_dir = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'pages')
    return send_from_directory(pages_dir, 'login.html')

@app.route('/signup')
def serve_signup():
    pages_dir = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'pages')
    return send_from_directory(pages_dir, 'signup.html')

@app.route('/dashboard')
def serve_dashboard():
    pages_dir = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'pages')
    return send_from_directory(pages_dir, 'dashboard.html')

@app.route('/static/styles/<path:filename>')
def serve_styles(filename):
    styles_dir = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'styles')
    return send_from_directory(styles_dir, filename)

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    js_dir = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'js')
    return send_from_directory(js_dir, filename)
# ============================================
# Entry Point
# ============================================
if __name__ == '__main__':
    app = create_app()
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Required for eventlet
    )