from functools import wraps
from flask import session, jsonify

def role_required(*allowed_roles):
    """
    Decorator to restrict access based on user role.
    Example usage:
        @role_required("admin")
        @role_required("customer", "admin")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("logged_in"):
                return jsonify({"status": "error", "message": "Login required"}), 401

            user_role = session.get("role")
            if user_role not in allowed_roles:
                return jsonify({"status": "error", "message": "Access denied"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
