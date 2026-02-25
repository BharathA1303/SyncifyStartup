"""
Auth API Routes
===============
/api/auth/login    - Verify Firebase token, return JWT
/api/auth/me       - Get current user
/api/auth/logout   - Invalidate session
"""
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from services.firebase_service import verify_firebase_token
from utils.auth_middleware import require_auth, generate_jwt
from utils.validators import validate_username, sanitize_text
from utils.helpers import success_response, error_response, utcnow
from flask_limiter import Limiter
from extensions import limiter

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """
    Verify Firebase ID token, create user if needed, return JWT.
    
    Body: { "token": "<firebase_id_token>" }
    Returns: { "jwt": "...", "user": {...} }
    """
    data = request.get_json()
    if not data or not data.get('token'):
        return jsonify(error_response('Firebase token required')[0]), 400

    # Verify Firebase token
    try:
        decoded = verify_firebase_token(data['token'])
    except ValueError as e:
        return jsonify(error_response(str(e))[0]), 401

    firebase_uid = decoded['uid']
    email = decoded.get('email', '')
    display_name = decoded.get('name', '')
    photo_url = decoded.get('picture', '')

    # Find or create user
    user = User.get_by_firebase_uid(firebase_uid)

    if not user:
        # Generate username from email
        base_username = email.split('@')[0].lower()
        base_username = ''.join(c for c in base_username if c.isalnum() or c == '_')[:25]
        username = base_username

        # Ensure uniqueness
        counter = 1
        while User.get_by_username(username):
            username = f"{base_username}{counter}"
            counter += 1

        user = User(
            firebase_uid=firebase_uid,
            username=username,
            email=email,
            bio='',
            profile_picture=photo_url,
        )
        db.session.add(user)
        db.session.commit()
        is_new_user = True
    else:
        is_new_user = False

    # Update last seen
    user.last_seen = utcnow()
    db.session.commit()

    # Generate JWT
    jwt_token = generate_jwt(user.id)

    return jsonify({
        'success': True,
        'jwt': jwt_token,
        'user': user.to_dict(include_private=True),
        'is_new_user': is_new_user
    }), 200


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_me():
    """Get current authenticated user."""
    from flask import g
    return jsonify(success_response(g.current_user.to_dict(include_private=True))[0]), 200


@auth_bp.route('/setup-profile', methods=['PUT'])
@require_auth
@limiter.limit("5 per minute")
def setup_profile():
    """
    Complete profile setup after first login.
    Body: { "username": "...", "bio": "..." }
    """
    from flask import g
    data = request.get_json()

    if not data:
        return jsonify(error_response('No data provided')[0]), 400

    user = g.current_user

    if 'username' in data:
        username = sanitize_text(data['username'], 30).lower()
        valid, msg = validate_username(username)
        if not valid:
            return jsonify(error_response(msg)[0]), 400

        existing = User.get_by_username(username)
        if existing and existing.id != user.id:
            return jsonify(error_response('Username already taken')[0]), 409

        user.username = username

    if 'bio' in data:
        user.bio = sanitize_text(data['bio'], 500)

    db.session.commit()
    return jsonify(success_response(user.to_dict(include_private=True))[0]), 200