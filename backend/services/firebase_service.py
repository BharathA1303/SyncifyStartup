"""
Firebase Service
================
Firebase Admin SDK wrapper.
Handles token verification and storage operations.
"""
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import storage
from flask import current_app
import uuid
import os


def verify_firebase_token(id_token):
    """
    Verify a Firebase ID token from the frontend.
    Returns decoded token payload or raises exception.
    
    Usage in auth routes:
        decoded = verify_firebase_token(request.json.get('token'))
        firebase_uid = decoded['uid']
        email = decoded.get('email')
    """
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except firebase_auth.ExpiredIdTokenError:
        raise ValueError("Token has expired")
    except firebase_auth.InvalidIdTokenError:
        raise ValueError("Invalid token")
    except Exception as e:
        raise ValueError(f"Token verification failed: {str(e)}")


def get_firebase_user(uid):
    """Get Firebase user record by UID."""
    try:
        return firebase_auth.get_user(uid)
    except Exception:
        return None


def upload_file_to_storage(file_data, destination_path, content_type='application/octet-stream'):
    """
    Upload a file to Firebase Storage.
    Returns the public download URL.
    
    Usage:
        url = upload_file_to_storage(file.read(), f'songs/{uuid}.mp3', 'audio/mpeg')
    """
    try:
        bucket = storage.bucket()
        blob = bucket.blob(destination_path)
        blob.upload_from_string(file_data, content_type=content_type)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        raise ValueError(f"Upload failed: {str(e)}")


def delete_file_from_storage(file_path):
    """Delete a file from Firebase Storage."""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        blob.delete()
        return True
    except Exception:
        return False


def upload_profile_picture(file_data, user_id, content_type='image/jpeg'):
    """Upload profile picture to Firebase Storage."""
    path = f"profile_pictures/{user_id}/{uuid.uuid4()}.jpg"
    return upload_file_to_storage(file_data, path, content_type)


def upload_song_file(file_data, filename, content_type='audio/mpeg'):
    """Upload song audio file to Firebase Storage."""
    ext = filename.rsplit('.', 1)[-1] if '.' in filename else 'mp3'
    path = f"songs/{uuid.uuid4()}.{ext}"
    return upload_file_to_storage(file_data, path, content_type)


def upload_song_cover(file_data, content_type='image/jpeg'):
    """Upload song cover image to Firebase Storage."""
    path = f"song_covers/{uuid.uuid4()}.jpg"
    return upload_file_to_storage(file_data, path, content_type)


def upload_voice_note(file_data, content_type='audio/webm'):
    """Upload voice note to Firebase Storage."""
    path = f"voice_notes/{uuid.uuid4()}.webm"
    return upload_file_to_storage(file_data, path, content_type)