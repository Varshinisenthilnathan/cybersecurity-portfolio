from datetime import datetime
from myapp.utils.db_utils import (
    insert_maid,
    get_maid_by_id,
    get_all_maids,
    update_maid,
    delete_maid
)

from myapp.utils.validators import validate_dob,validate_email,calculate_age

def register_maid(data):
    name = data.get("name")
    phone_number = data.get("phone_number")
    address = data.get("address")
    email = data.get("email")
    gender = data.get("gender")
    dob = data.get("dob")
    age = data.get("age")
    experience_years = data.get("experience_years")
    service = data.get("service")
    salary = data.get("salary", 0.0)
    created_by = data.get("created_by", "system")

    if not all([name, phone_number, gender, service]):
        return {"status": "error", "message": "Missing required fields"}
    
    if email and not validate_email(email):
        return {"status": "error", "message": "Invalid email format"}, 400
  
    if gender not in ['Male', 'Female', 'Other']:
        return {"status": "error", "message": "Gender must be Male, Female, or Other"}, 400

    if dob:
        is_valid, result = validate_dob(dob)
        if not is_valid:
            return {"status": "error", "message": result}, 400
        dob = result

    try:
        experience_years = int(experience_years) if experience_years else 0
        if experience_years < 0:
            return {"status": "error", "message": "Experience years cannot be negative"}, 400
    except ValueError:
        return {"status": "error", "message": "Invalid experience years"}, 400

    try:
        salary = float(salary) if salary else 0.0
        if salary < 0:
            return {"status": "error", "message": "Salary cannot be negative"}, 400
    except ValueError:
        return {"status": "error", "message": "Invalid salary format"}, 400

    success, error = insert_maid(
        name, phone_number, address, email, gender, dob, age,
        experience_years, service, salary, created_by
    )

    if not success:
        return {"status": "error", "message": f"Failed to create maid: {error}"}
    return {"status": "success", "message": "Maid registered successfully."}

# retrive by id
def get_maid_by_id_service(maid_id):
    if not maid_id or maid_id <= 0:
        return {"status": "error", "message": "Invalid maid ID"}, 400
    
    maid, error = get_maid_by_id(maid_id)
    
    if error:
        if error == "Maid not found":
            return {"status": "error", "message": error}, 404
        return {"status": "error", "message": error}, 500
    
    return {"status": "success", "data": maid}, 200

# retreive all maid
def get_all_maids_service(filters=None):
    if filters:
        if filters.get('availability_status'):
            if filters['availability_status'] not in ['AVAILABLE', 'BOOKED', 'INACTIVE']:
                return {"status": "error", "message": "Invalid availability status"}, 400
        
        if filters.get('gender'):
            if filters['gender'] not in ['Male', 'Female', 'Other']:
                return {"status": "error", "message": "Invalid gender"}, 400
    
    maids, error = get_all_maids(filters)
    
    if error:
        return {"status": "error", "message": error}, 500
    
    return {
        "status": "success", 
        "count": len(maids),
        "data": maids
    }, 200

# update maid
def update_maid_service(maid_id, data):
    if not maid_id or maid_id <= 0:
        return {"status": "error", "message": "Invalid maid ID"}, 400
    
    if not data or len(data) == 0:
        return {"status": "error", "message": "No data provided for update"}, 400
    
    update_data = {}
    if 'name' in data:
        name = data['name'].strip()
        if not name:
            return {"status": "error", "message": "Name cannot be empty"}, 400
        update_data['name'] = name
    
    if 'phone_number' in data:
        phone_number = data['phone_number'].strip()
        update_data['phone_number'] = phone_number
    
    if 'address' in data:
        update_data['address'] = data['address'].strip()
    
    if 'email' in data:
        email = data['email'].strip() if data['email'] else None
        if email and not validate_email(email):
            return {"status": "error", "message": "Invalid email format"}, 400
        update_data['email'] = email
    
    if 'gender' in data:
        gender = data['gender']
        if gender not in ['Male', 'Female', 'Other']:
            return {"status": "error", "message": "Gender must be Male, Female, or Other"}, 400
        update_data['gender'] = gender
    
    if 'dob' in data:
        dob_str = data['dob']
        if dob_str:
            is_valid, result = validate_dob(dob_str)
            if not is_valid:
                return {"status": "error", "message": result}, 400
            update_data['dob'] = result
            update_data['age'] = calculate_age(result)
    
    if 'age' in data and 'dob' not in data:
        try:
            age = int(data['age'])
            if age < 0 or age > 100:
                return {"status": "error", "message": "Invalid age"}, 400
            update_data['age'] = age
        except ValueError:
            return {"status": "error", "message": "Invalid age format"}, 400
    
    if 'experience_years' in data:
        try:
            exp = int(data['experience_years'])
            if exp < 0:
                return {"status": "error", "message": "Experience years cannot be negative"}, 400
            update_data['experience_years'] = exp
        except ValueError:
            return {"status": "error", "message": "Invalid experience years"}, 400
    
    if 'service' in data:
        service = data['service'].strip()
        if not service:
            return {"status": "error", "message": "Service cannot be empty"}, 400
        update_data['service'] = service
    
    if 'salary' in data:
        try:
            salary = float(data['salary'])
            if salary < 0:
                return {"status": "error", "message": "Salary cannot be negative"}, 400
            update_data['salary'] = salary
        except ValueError:
            return {"status": "error", "message": "Invalid salary format"}, 400
    
    if 'availability_status' in data:
        status = data['availability_status']
        if status not in ['AVAILABLE', 'BOOKED', 'INACTIVE']:
            return {"status": "error", "message": "Invalid availability status"}, 400
        update_data['availability_status'] = status
    update_data['updated_by'] = data.get('updated_by', 'system')
    success, error = update_maid(maid_id, update_data)
    
    if not success:
        if error == "Maid not found":
            return {"status": "error", "message": error}, 404
        return {"status": "error", "message": error}, 400
    return {
        "status": "success",
        "message": f"Maid ID {maid_id} updated successfully",
        "updated_fields": list(update_data.keys())
    }, 200

# delete maid
def delete_maid_service(maid_id, deleted_by="system"):
 
    if not maid_id or maid_id <= 0:
        return {"status": "error", "message": "Invalid maid ID"}, 400
    
    success, error = delete_maid(maid_id, deleted_by)
    if not success:
        if error == "Maid not found or already deleted":
            return {"status": "error", "message": error}, 404
        return {"status": "error", "message": error}, 400

    return {
        "status": "success",
        "message": f"Maid ID deleted successfully ",
        "deleted_by": deleted_by
    }, 200