"""
Input Validators & Sanitizers
==============================
Sanitize all user input before DB operations.
"""
import bleach
import re
import os


ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}


def sanitize_text(text, max_length=None):
    """Strip HTML tags and dangerous content from text."""
    if not text:
        return ''
    cleaned = bleach.clean(str(text), tags=[], strip=True)
    cleaned = cleaned.strip()
    if max_length:
        cleaned = cleaned[:max_length]
    return cleaned


def validate_username(username):
    """Username: 3-30 chars, alphanumeric + underscores."""
    if not username:
        return False, 'Username is required'
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    if not re.match(pattern, username):
        return False, 'Username must be 3-30 chars, letters/numbers/underscores only'
    return True, None


def validate_email(email):
    """Basic email format validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not re.match(pattern, email):
        return False, 'Invalid email address'
    return True, None


def validate_audio_file(filename):
    """Check if uploaded file is an allowed audio format."""
    if not filename or '.' not in filename:
        return False, 'Invalid filename'
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        return False, f'Audio must be one of: {", ".join(ALLOWED_AUDIO_EXTENSIONS)}'
    return True, None


def validate_image_file(filename):
    """Check if uploaded file is an allowed image format."""
    if not filename or '.' not in filename:
        return False, 'Invalid filename'
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False, f'Image must be one of: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
    return True, None


def validate_mood_tag(mood):
    """Validate mood against allowed values."""
    allowed_moods = {'chill', 'study', 'gym', 'party', 'late_night', 
                     'happy', 'sad', 'energetic', 'romantic', 'focus'}
    if mood not in allowed_moods:
        return False, f'Mood must be one of: {", ".join(allowed_moods)}'
    return True, None


def validate_genre(genre):
    """Validate genre against allowed values."""
    allowed_genres = {
        'pop', 'rock', 'hip_hop', 'rnb', 'electronic', 'jazz',
        'classical', 'indie', 'metal', 'country', 'reggae', 'latin',
        'soul', 'funk', 'blues', 'folk', 'alternative', 'ambient'
    }
    if genre not in allowed_genres:
        return False, f'Invalid genre'
    return True, None


def sanitize_message(text):
    """Sanitize chat message content."""
    return sanitize_text(text, max_length=2000)


def sanitize_bio(bio):
    """Sanitize user bio."""
    return sanitize_text(bio, max_length=500)


def sanitize_playlist_name(name):
    """Sanitize playlist name."""
    return sanitize_text(name, max_length=100)