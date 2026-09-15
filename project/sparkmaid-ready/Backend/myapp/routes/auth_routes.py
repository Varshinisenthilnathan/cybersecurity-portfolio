from flask import Blueprint, request,session
from myapp.service.auth_service import login_user_service,reset_password_common,forgot_password_common
from myapp.utils.db_utils import get_admin_by_email,get_customer_by_email


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Call your existing service
    response, status_code = login_user_service(role, email, password)

    # If login successful → store session
    if response["status"] == "success":
        session["user_id"] = response["user_id"]
        session["name"] = response["name"]
        session["role"] = role
        session["logged_in"] = True
        response["id"] = response["user_id"]
        response["role"] = role
        response["email"] = email

    return response, status_code

@auth_bp.route('/forgotpassword', methods=['POST'])
def forgot_password_route():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return {"status": "error", "message": "Email is required"}, 400

    return forgot_password_common(email)


@auth_bp.route('/resetpassword', methods=['POST'])
def reset_password_route():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("new_password")

    if not email or not new_password:
        return {"status": "error", "message": "Email and new password are required"}, 400

    return reset_password_common(email, otp, new_password)


@auth_bp.route('/check-user-role', methods=['POST'])
def check_user_role():
    data = request.get_json()
    email = data.get("email")

    if get_customer_by_email(email):
        return {"role": "customer"}
    elif get_admin_by_email(email):
        return {"role": "admin"}
    return {"role": "unknown"}
