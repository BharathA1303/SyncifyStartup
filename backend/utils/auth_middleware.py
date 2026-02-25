"""
Authentication Middleware
=========================
JWT verification + Firebase token validation.
Attach to any route with @require_auth decorator.
"""
import jwt
import os
from functools import wraps
from flask import request, jsonify, current_app, g
from models.user import User


def require_auth(f):
    """
    Decorator to protect routes.
    Verifies JWT, loads user into g.current_user.
    
    Usage:
        @app.route('/api/protected')
        @require_auth
        def protected_route():
            user = g.current_user
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_token(request)
        if not token:
            return jsonify({'error': 'No token provided'}), 401

        payload = _verify_jwt(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        user = User.query.filter_by(id=payload.get('user_id')).first()
        if not user:
            return jsonify({'error': 'User not found'}), 401

        g.current_user = user
        g.user_id = str(user.id)
        return f(*args, **kwargs)

    return decorated


def require_auth_ws(data):
    """
    WebSocket authentication.
    Call at start of any SocketIO event handler.
    Returns user or None.
    """
    token = data.get('token') if data else None
    if not token:
        return None

    payload = _verify_jwt(token)
    if not payload:
        return None

    return User.query.filter_by(id=payload.get('user_id')).first()


def _extract_token(request):
    """Extract Bearer token from Authorization header."""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return None


def _verify_jwt(token):
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_jwt(user_id):
    """
    Generate JWT for a user.
    Called after Firebase token verification.
    """
    import datetime
    payload = {
        'user_id': str(user_id),
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            seconds=current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)
        )
    }
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )