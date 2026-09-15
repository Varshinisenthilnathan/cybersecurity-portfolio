import hashlib
from datetime import datetime
from myapp.utils.email_utils import generate_otp, send_otp_email
from myapp.utils.db_utils import (
    insert_customer,
    get_customer_by_email,
    activate_customer,
    get_all_customers,
     get_customer_by_id,
     update_customer,
     soft_delete_customer
)

from myapp.utils.validators import validate_dob
# --------------- REGISTER CUSTOMER ---------------- #
def register_customer(data):
    """Register new customer with OTP verification"""
    name = data.get("name")
    phone_number = data.get("phone_number")
    address = data.get("address")
    email = data.get("email")
    gender = data.get("gender")
    age = data.get("age")
    dob = data.get("dob")
    username = data.get("username")
    password = data.get("password")
    service_registered = data.get("service_registered")  
    created_by = data.get("created_by", "system")
    if dob:
        is_valid, result = validate_dob(dob)
        if not is_valid:
            return {"status": "error", "message": result}, 400
        dob = result

    if not all([name, phone_number, email, username, password, service_registered]):
        return {"status": "error", "message": "Missing required fields"}
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    otp = generate_otp()
    success, error = insert_customer(
        name, phone_number, address, email, gender, dob, age,
         username, hashed_password, otp, created_by, service_registered
    )
    if not success:
        return {"status": "error", "message": error}
    if not send_otp_email(email, otp):
        return {"status": "error", "message": "Failed to send OTP email"}

    return {"status": "success", "message": "Customer registered successfully. Please verify OTP."}


# ---------------- VERIFY OTP ---------------- #
def verify_otp(email, otp):
    """Verify OTP and activate account if not expired"""
    customer = get_customer_by_email(email)
    print(email)
    if not customer:
        return {"status": "error", "message": "Customer not found"}

    if customer["status"] == "ACTIVE" :
        return {"status": "error", "message": "Customer already verified"}

    print(f"DB OTP: {customer['otp']} | Input OTP: {otp}")
  
    if (customer["otp"]) != (otp):
        return {"status": "error", "message": "Invalid OTP"}

    if not customer["otp_expiry"] or datetime.now() > customer["otp_expiry"]:
        return {"status": "error", "message": "OTP expired. Please request a new one"}

    if customer["status"] == "PENDING":
        activate_customer(email)

    return {"status": "success", "message": "OTP verified successfully."}




# retirve all customer
def get_all_customer():

    customers, error = get_all_customers()
    if error:
        return {"status": "error", "message": error}, 500
    
    if not customers:
        return {"status": "success", "message": "No customers found", "data": []}, 200
    
    return {"status": "success", "data": customers}, 200

# retrive by id
def get_customers_by_id(customer_id):
    if not customer_id or customer_id <= 0:
        return {"status": "error", "message": "Invalid customer ID"}, 400
    
    customer, error = get_customer_by_id(customer_id)
    if error:
        return {"status": "error", "message": error}, 500
    
    if not customer:
        return {"status": "error", "message": "Customer not found"}, 404
    
    return {"status": "success", "data": customer}, 200

# update customer
def update_customers(customer_id, data):
    if not data:
        return {"status": "error", "message": "No data provided"}

    success, error = update_customer(customer_id, data)
    if error:
        if error == "No changes made":
            return {"status": "info", "message": "No changes made"}
        return {"status": "error", "message": error}

    return {"status": "success", "message": "Customer updated successfully"}
# delete customer
def delete_customer(customer_id, deleted_by="system"):
    """Soft delete a customer"""
    success, error = soft_delete_customer(customer_id, deleted_by)
    if error:
        return {"status": "error", "message": error}

    return {"status": "success", "message": "Customer deleted successfully"}
