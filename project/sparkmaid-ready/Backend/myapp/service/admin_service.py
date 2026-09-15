import hashlib
from myapp.utils.db_utils import insert_admin,get_all_admins,update_admin_details
from datetime import datetime
from myapp.utils.validators import validate_dob
def register_admin(data):
    """Register new admin with OTP verification"""
    name = data.get("name")
    phone_number = data.get("phone_number")
    address = data.get("address")
    email = data.get("email")
    gender = data.get("gender")
    dob = data.get("dob")
    age = data.get("age")
    username = data.get("username")
    password = data.get("password")
    created_by = data.get("created_by", "system")

    if dob:
        is_valid, result = validate_dob(dob)
        if not is_valid:
            return {"status": "error", "message": result}, 400
        dob = result

    if not all([name, email, username, password]):
        return {"status":"error","message":"Missing required fields"}

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
   
    success, error = insert_admin(name, phone_number, address, email, gender, dob, age, username, hashed_password, created_by)
    if not success:
        return {"status":"error","message":error}

    return {"status":"success","message":"Admin registered successfully."}

# retrive all admins
def get_all_admins_service():
    admins, error = get_all_admins()
    if error:
        return {"status": "error", "message": error}, 500
    if not admins:
        return {"status": "success", "message": "No admins found", "data": []}, 200
    return {"status": "success", "data": admins}, 200

# update admin details
def update_admin_service(admin_id, update_data):
    if not admin_id or admin_id <= 0:
        return {"status": "error", "message": "Invalid admin ID"}, 400

    if not update_data:
        return {"status": "error", "message": "No data provided for update"}, 400

    result, error = update_admin_details(admin_id, update_data)
    if error:
        return {"status": "error", "message": error}, 500

    if result == "no_change":
        return {"status": "success", "message": "No changes detected"}, 200

    return {"status": "success", "message": "Admin details updated successfully"}, 200