# auth/decorators.py
from functools import wraps
from flask import redirect, url_for, flash, abort, current_app
from .service import get_current_user

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = get_current_user()
        if not user:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login_form"))
        return view(*args, **kwargs)
    return wrapped

def role_required(*allowed_role_ids):
    """
    Usage:
        @role_required(2)          # only admins
        @role_required(1, 2)       # users & admins
    """
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = get_current_user()
            if not user:
                # Not authenticated → go to login
                flash("Please log in to continue.", "error")
                return redirect(url_for("auth.login_form"))

            role_id = user.get("role_id")
            if role_id not in allowed_role_ids:
                # Authenticated but not authorized → 403 or safe redirect
                # Preferred: return a proper 403
                abort(403)

              

            return view(*args, **kwargs)
        return wrapped
    return decorator