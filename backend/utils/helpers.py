"""
Utility Helper Functions
========================
Reusable helpers across the entire backend.
"""
import uuid
import random
import string
from datetime import datetime, timezone


def generate_uuid():
    """Generate a new UUID4 string."""
    return str(uuid.uuid4())


def generate_session_code(length=8):
    """Generate a unique sync session code (e.g. SYNC-A3K9)."""
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(chars, k=length))
    return f"SYNC-{code[:4]}"


def utcnow():
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def success_response(data=None, message='Success', status=200):
    """Standard success JSON response."""
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return response, status


def error_response(message='An error occurred', status=400, errors=None):
    """Standard error JSON response."""
    response = {'success': False, 'error': message}
    if errors:
        response['errors'] = errors
    return response, status


def paginate_query(query, page=1, per_page=20):
    """Paginate a SQLAlchemy query."""
    page = max(1, int(page))
    per_page = min(100, max(1, int(per_page)))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': pagination.items,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
    }


def calculate_bond_level(snap_points):
    """
    Convert snap points to bond level name.
    
    Levels:
    0-99     → New Vibes
    100-499  → Music Buddies  
    500-1499 → Soul Sync
    1500+    → Legendary Bond
    """
    if snap_points >= 1500:
        return {'name': 'Legendary Bond', 'tier': 4, 'color': '#FFD700'}
    elif snap_points >= 500:
        return {'name': 'Soul Sync', 'tier': 3, 'color': '#7f5af0'}
    elif snap_points >= 100:
        return {'name': 'Music Buddies', 'tier': 2, 'color': '#2cb67d'}
    else:
        return {'name': 'New Vibes', 'tier': 1, 'color': '#94a1b2'}


def format_duration(seconds):
    """Format seconds into MM:SS or HH:MM:SS string."""
    seconds = int(seconds)
    if seconds >= 3600:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h}:{m:02d}:{s:02d}"
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}"


def safe_int(value, default=0):
    """Safely convert to int with fallback."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """Safely convert to float with fallback."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default