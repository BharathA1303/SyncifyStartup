"""
SYNCIFY Backend — Flask Application Entry Point
"""
import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, jsonify, send_from_directory
from config.settings import get_config
from extensions import db, socketio, limiter, cors, migrate, init_redis

import models  # noqa
import socket_events  # noqa


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or get_config())

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

    init_redis(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_pages(app)
    init_firebase(app)

    if not app.config.get('TESTING'):
        init_scheduler(app)

    return app


def register_blueprints(app):
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

    app.register_blueprint(auth_bp,        url_prefix='/api/auth')
    app.register_blueprint(users_bp,       url_prefix='/api/users')
    app.register_blueprint(songs_bp,       url_prefix='/api/songs')
    app.register_blueprint(playlists_bp,   url_prefix='/api/playlists')
    app.register_blueprint(messages_bp,    url_prefix='/api/messages')
    app.register_blueprint(sync_bp,        url_prefix='/api/sync')
    app.register_blueprint(snaps_bp,       url_prefix='/api/snaps')
    app.register_blueprint(rooms_bp,       url_prefix='/api/rooms')
    app.register_blueprint(challenges_bp,  url_prefix='/api/challenges')
    app.register_blueprint(ai_bp,          url_prefix='/api/ai')


def register_error_handlers(app):
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


def register_pages(app):
    """Serve frontend HTML pages in development."""
    import os as _os

    def pages_dir():
        return _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'pages')

    def styles_dir():
        return _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'styles')

    def js_dir():
        return _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'frontend', 'js')

    pages = [
        ('/', 'index.html'),
        ('/login', 'login.html'),
        ('/signup', 'signup.html'),
        ('/dashboard', 'dashboard.html'),
        ('/profile', 'profile.html'),
        ('/friends', 'friends.html'),
        ('/chat', 'chat.html'),
        ('/sync', 'sync.html'),
        ('/rooms', 'rooms.html'),
        ('/playlists', 'playlists.html'),
        ('/challenges', 'challenges.html'),
        ('/timeline', 'timeline.html'),
        ('/compatibility', 'compatibility.html'),
    ]

    for route, filename in pages:
        # Create a closure to capture filename correctly
        def make_view(fn):
            def view():
                return send_from_directory(pages_dir(), fn)
            view.__name__ = 'page_' + fn.replace('.', '_')
            return view

        app.add_url_rule(route, view_func=make_view(filename))
        app.add_url_rule(route + '.html', view_func=make_view(filename),
                         endpoint='page_html_' + filename.replace('.', '_'))

    @app.route('/static/styles/<path:filename>')
    def serve_styles(filename):
        return send_from_directory(styles_dir(), filename)

    @app.route('/static/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(js_dir(), filename)


def init_firebase(app):
    try:
        import firebase_admin
        from firebase_admin import credentials

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
    try:
        from services.scheduler import start_scheduler
        start_scheduler(app)
        app.logger.info("✅ Scheduler initialized")
    except Exception as e:
        app.logger.warning(f"⚠️  Scheduler not started: {e}")


if __name__ == '__main__':
    app = create_app()
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )