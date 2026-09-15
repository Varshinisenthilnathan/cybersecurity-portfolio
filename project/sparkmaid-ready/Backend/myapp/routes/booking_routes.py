from flask import Blueprint, request
from myapp.utils.db_utils import create_booking_table
from myapp.service.booking_service import create_booking_service, get_customer_booking_history_service, get_all_booking_history_service,update_booking_service,get_booking_history_service
from myapp.utils.auth_decorators import role_required 

booking_bp = Blueprint('booking', __name__)

create_booking_table()

# API to create a new booking
@booking_bp.route('/booking', methods=['POST'])
@role_required("admin", "customer")
def create_booking_route():
    data = request.get_json()
    return create_booking_service(data)

# API to get a customer's booking history
@booking_bp.route('/booking/customer/<int:customer_id>', methods=['GET'])
@role_required("admin", "customer")
def get_customer_booking_route(customer_id):
    return get_customer_booking_history_service(customer_id)

# API to get all bookings (admin)
@booking_bp.route('/booking/admin', methods=['GET'])
@role_required("admin")
def get_all_booking_route():
    return get_all_booking_history_service()

# update booking service
@booking_bp.route('/booking/<int:booking_id>', methods=['PUT'])
@role_required("admin")
def update_booking_route(booking_id):
    data = request.get_json()
    return update_booking_service(booking_id, data)

# API to get a customer's booking history
@booking_bp.route('/booking/<int:booking_id>', methods=['GET'])
@role_required("admin")
def get_booking_route(booking_id):
    return get_booking_history_service(booking_id)