import hashlib
from datetime import datetime, timedelta
from myapp.utils.db_utils import (
    get_connection,
    get_customer_by_email,
    get_admin_by_email,
    update_customer_otp,
    update_customer_password,
    update_admin_password

)
from myapp.utils.email_utils import send_otp_email, generate_otp


def login_user_service(role, email, password):

    conn = get_connection()
    if not conn:
        return {"status": "error", "message": "Database connection failed"}, 500

    try:
        cursor = conn.cursor(dictionary=True)

        if role == "customer":
            cursor.execute("SELECT * FROM customer WHERE email = %s AND deleted_date IS NULL", (email,))
        elif role == "admin":
            cursor.execute("SELECT * FROM admin WHERE email = %s AND deleted_date IS NULL", (email,))
        else:
            return {"status": "error", "message": "Invalid role type"}, 400

        user = cursor.fetchone()

        if not user:
            return {"status": "error", "message": "User not found"}, 404

        if hashlib.sha256(password.encode()).hexdigest() != user["password"]:
             return {"status": "error", "message": "Incorrect password"}, 401
        return {
            "status": "success",
            "message": f"{role.capitalize()} login successful",
            "user_id": user.get(f"{role}_id"),
            "name": user.get("name")
        }, 200

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    finally:
        cursor.close()
        conn.close()



def forgot_password_common(email):
    """Handles forgot password for both customer and admin"""
    # Check if user is a customer
    customer = get_customer_by_email(email)
    if customer:
        otp = generate_otp()
        if not update_customer_otp(email, otp):
            return {"status": "error", "message": "Failed to update OTP"}
        if not send_otp_email(email, otp):
            return {"status": "error", "message": "Failed to send OTP email"}
        return {"status": "success", "message": f"OTP sent to {email} for password reset"}

    # Check if user is an admin
    admin = get_admin_by_email(email)
    if admin:
        # For admin, send only a reset notification link or info (no OTP)
        return {"status": "success", "message": f"Reset instructions sent to admin email {email}"}

    return {"status": "error", "message": "Email not found in system"}


def reset_password_common(email, otp, new_password):
    """Handles reset password for both customer and admin"""
    customer = get_customer_by_email(email)
    admin = get_admin_by_email(email)
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    # --- CUSTOMER FLOW (with OTP validation) ---
    if customer:
        if not customer.get("otp") or customer["otp"] != otp:
            return {"status": "error", "message": "Invalid OTP"}
        if not customer.get("otp_expiry") or datetime.now() > customer["otp_expiry"]:
            return {"status": "error", "message": "OTP expired. Please request a new one"}

        if not update_customer_password(email, hashed_password):
            return {"status": "error", "message": "Failed to update password"}
        return {"status": "success", "message": "Customer password reset successful"}

    # --- ADMIN FLOW (no OTP required) ---
    if admin:
        if not update_admin_password(email, hashed_password):
            return {"status": "error", "message": "Failed to update admin password"}
        return {"status": "success", "message": "Admin password reset successful"}

    return {"status": "error", "message": "Email not found in system"}

