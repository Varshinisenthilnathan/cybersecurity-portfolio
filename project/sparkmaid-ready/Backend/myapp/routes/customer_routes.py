from flask import Blueprint, request
from myapp.utils.db_utils import create_customer_table
from myapp.service.customer_service import (register_customer,
                                             verify_otp,
                                            get_all_customer,
                                            get_customers_by_id,
                                            update_customers,
                                            delete_customer)

from myapp.utils.auth_decorators import role_required 

customer_bp = Blueprint('customer_bp', __name__)

create_customer_table()
 # Register Customer
@customer_bp.route('/customer/register', methods=['POST'])
#@role_required("customer", "admin")
def register_customer_route():
        data = request.get_json()
        return register_customer(data)

# Verify OTP
@customer_bp.route('/customer/verifyotp', methods=['POST'])
#@role_required("customer", "admin")
def verify_customer_otp_route():
        data = request.get_json()
        email = data.get("email")
        otp = data.get("otp")
        return verify_otp(email, otp)
    

# retrieve a;; customer
@customer_bp.route('/customers', methods=['GET'])
@role_required("admin")
def get_all_customers_route():
    print("start")
    return get_all_customer()

# retrieve CUSTOMER BY ID 
@customer_bp.route('/customer/<int:customer_id>', methods=['GET'])
@role_required("admin", "customer")
def get_customer_by_id_route(customer_id):
    return get_customers_by_id(customer_id)

# update customer details
@customer_bp.route("/customer/<int:customer_id>", methods=["PUT"])
@role_required("admin", "customer")
def update_customer_route(customer_id):
    data = request.get_json()
    return update_customers(customer_id, data)

# soft delete customer details
@customer_bp.route("/customer/<int:customer_id>", methods=["DELETE"])
@role_required("admin")
def delete_customer_route(customer_id):
        data = request.get_json(silent=True)
        deleted_by = data.get("deleted_by", "system") if data else "system"
        return delete_customer(customer_id, deleted_by)


    # Login
    # @app.route('/customer/login', methods=['POST'])
    # def login_customer_route():
    #     data = request.get_json()
    #     username = data.get("username")
    #     password = data.get("password")
    #     return login(username, password)

    # # Resend OTP
    # @app.route('/customer/resend-otp', methods=['POST'])
    # def resend_customer_otp_route():
    #     data = request.get_json()
    #     email = data.get("email")
    #     return resend_otp(email)

