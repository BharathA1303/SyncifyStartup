"""
Users API Routes
================
Full user profile + friends system.
"""
from flask import Blueprint, request, jsonify, g
from extensions import db
from models.user import User
from models.friendship import Friendship
from models.snap import SnapTransaction
from models.sync_session import SyncSession
from utils.auth_middleware import require_auth
from utils.validators import validate_username, sanitize_text, sanitize_bio, validate_image_file
from utils.helpers import success_response, error_response, utcnow
from extensions import limiter

users_bp = Blueprint('users', __name__)


@users_bp.route('/profile', methods=['GET'])
@require_auth
def get_own_profile():
    user = g.current_user
    return jsonify({**user.to_dict(include_private=True), 'stats': _get_user_stats(user.id)}), 200


@users_bp.route('/profile', methods=['PUT'])
@require_auth
@limiter.limit("10 per minute")
def update_profile():
    user = g.current_user
    data = request.get_json()
    if not data:
        return jsonify(error_response('No data')[0]), 400
    if 'username' in data:
        username = sanitize_text(data['username'], 30).lower()
        valid, msg = validate_username(username)
        if not valid:
            return jsonify(error_response(msg)[0]), 400
        existing = User.get_by_username(username)
        if existing and str(existing.id) != str(user.id):
            return jsonify(error_response('Username taken')[0]), 409
        user.username = username
    if 'bio' in data:
        user.bio = sanitize_bio(data['bio'])
    db.session.commit()
    return jsonify(success_response(user.to_dict(include_private=True))[0]), 200


@users_bp.route('/profile/avatar', methods=['POST'])
@require_auth
@limiter.limit("5 per minute")
def upload_avatar():
    user = g.current_user
    if 'file' not in request.files:
        return jsonify(error_response('No file')[0]), 400
    file = request.files['file']
    valid, msg = validate_image_file(file.filename)
    if not valid:
        return jsonify(error_response(msg)[0]), 400
    try:
        from services.firebase_service import upload_profile_picture
        url = upload_profile_picture(file.read(), str(user.id), file.content_type or 'image/jpeg')
        user.profile_picture = url
        db.session.commit()
        return jsonify(success_response({'profile_picture': url})[0]), 200
    except Exception as e:
        return jsonify(error_response(f'Upload failed: {str(e)}')[0]), 500


@users_bp.route('/<user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(error_response('User not found', 404)[0]), 404
    data = user.to_dict()
    data['stats'] = _get_user_stats(user_id)
    if str(user_id) != str(g.user_id):
        friendship = Friendship.get_friendship(g.user_id, user_id)
        data['friendship_status'] = friendship.status if friendship else None
        data['friendship_id'] = friendship.id if friendship else None
    return jsonify(data), 200


@users_bp.route('/search', methods=['GET'])
@require_auth
@limiter.limit("30 per minute")
def search_users():
    query = sanitize_text(request.args.get('q', ''), 50)
    if len(query) < 2:
        return jsonify(error_response('Query too short')[0]), 400
    users = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.id != g.user_id,
        User.is_active == True
    ).limit(20).all()
    return jsonify([u.to_public_dict() for u in users]), 200


@users_bp.route('/friends', methods=['GET'])
@require_auth
def get_friends():
    friends = Friendship.query.filter(
        db.or_(Friendship.requester_id == g.user_id, Friendship.receiver_id == g.user_id),
        Friendship.status == 'accepted'
    ).all()
    return jsonify([f.to_dict_with_user(g.user_id) for f in friends]), 200


@users_bp.route('/friends/pending', methods=['GET'])
@require_auth
def get_pending():
    pending = Friendship.query.filter_by(receiver_id=g.user_id, status='pending').all()
    return jsonify([f.to_dict_with_user(g.user_id) for f in pending]), 200


@users_bp.route('/friends/<target_id>', methods=['POST'])
@require_auth
@limiter.limit("20 per minute")
def send_request(target_id):
    if str(target_id) == str(g.user_id):
        return jsonify(error_response('Cannot friend yourself')[0]), 400
    if not User.query.get(target_id):
        return jsonify(error_response('User not found', 404)[0]), 404
    if Friendship.get_friendship(g.user_id, target_id):
        return jsonify(error_response('Already exists')[0]), 409
    f = Friendship(requester_id=g.user_id, receiver_id=target_id)
    db.session.add(f)
    db.session.commit()
    return jsonify(success_response(f.to_dict(), 'Request sent')[0]), 201


@users_bp.route('/friends/<friendship_id>/respond', methods=['PUT'])
@require_auth
def respond_request(friendship_id):
    f = Friendship.query.get(friendship_id)
    if not f or str(f.receiver_id) != str(g.user_id):
        return jsonify(error_response('Not found or unauthorized', 404)[0]), 404
    action = request.get_json().get('action')
    if action == 'accept':
        f.status = 'accepted'
        f.last_interaction_date = utcnow().date()
        db.session.commit()
        return jsonify(success_response(f.to_dict(), 'Accepted')[0]), 200
    elif action == 'reject':
        f.status = 'rejected'
        db.session.commit()
        return jsonify(success_response(message='Rejected')[0]), 200
    return jsonify(error_response('Invalid action')[0]), 400


@users_bp.route('/friends/<friendship_id>', methods=['DELETE'])
@require_auth
def remove_friend(friendship_id):
    f = Friendship.query.get(friendship_id)
    if not f:
        return jsonify(error_response('Not found', 404)[0]), 404
    if str(f.requester_id) != str(g.user_id) and str(f.receiver_id) != str(g.user_id):
        return jsonify(error_response('Unauthorized', 403)[0]), 403
    db.session.delete(f)
    db.session.commit()
    return jsonify(success_response(message='Removed')[0]), 200


def _get_user_stats(user_id):
    friend_count = Friendship.query.filter(
        db.or_(Friendship.requester_id == user_id, Friendship.receiver_id == user_id),
        Friendship.status == 'accepted'
    ).count()
    sync_count = SyncSession.query.filter(
        db.or_(SyncSession.host_id == user_id, SyncSession.guest_id == user_id),
        SyncSession.is_active == False
    ).count()
    total_points = db.session.query(
        db.func.sum(SnapTransaction.points_added)
    ).filter_by(user1_id=user_id).scalar() or 0
    return {'friend_count': friend_count, 'sync_sessions': sync_count, 'total_snap_points': total_points}