from functools import wraps
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash('Access denied.', 'error')
                return redirect(url_for('auth.index'))
            return f(*args, **kwargs)
        return decorated
    return decorator


ALLOWED_IMAGES = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_CVS = {'pdf', 'doc', 'docx'}


def save_uploaded_file(file, subfolder, prefix, allowed_extensions=None):
    if not file or not file.filename:
        return None
    allowed_extensions = allowed_extensions or ALLOWED_IMAGES
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed_extensions:
        return None
    try:
        filename = secure_filename(f"{prefix}_{int(datetime.utcnow().timestamp())}.{ext}")
        folder = os.path.join(current_app.root_path, 'static', 'uploads', subfolder)
        os.makedirs(folder, exist_ok=True)
        file.save(os.path.join(folder, filename))
        return f"/static/uploads/{subfolder}/{filename}"
    except Exception:
        return None
