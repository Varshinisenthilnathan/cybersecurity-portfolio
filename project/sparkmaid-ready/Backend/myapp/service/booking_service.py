# 
from myapp.utils.db_utils import insert_booking, get_booking_history_by_customer, get_all_booking_history,update_booking,get_booking_history

# create new bookig
def create_booking_service(data):
    customer_id = data.get("customer_id")
    maid_id = data.get("maid_id")
    service = data.get("service")
    duration = data.get("duration", 0)
    payment = data.get("payment", 0.0)
    created_by = data.get("created_by", "system")

    if not all([customer_id, maid_id, service]):
        return {"status": "error", "message": "Missing required fields"}, 400

    success, error = insert_booking(customer_id, maid_id, service, duration, payment, created_by)
    if not success:
        return {"status": "error", "message": error}, 400

    return {"status": "success", "message": "Booking created successfully"}, 201

# get by customer id
def get_customer_booking_history_service(customer_id):
    bookings, error = get_booking_history_by_customer(customer_id)
    if error:
        return {"status": "error", "message": error}, 400
    return {"status": "success", "bookings": bookings}, 200

# get all booking for admin
def get_all_booking_history_service():
    bookings, error = get_all_booking_history()
    if error:
        return {"status": "error", "message": error}, 400
    return {"status": "success", "bookings": bookings}, 200

# update booking serviec 
def update_booking_service(booking_id, data):
    if not booking_id or booking_id <= 0:
        return {"status": "error", "message": "Invalid booking ID"}, 400
    if not data or len(data) == 0:
        return {"status": "error", "message": "No data provided for update"}, 400
    if 'status' in data:
        if data['status'] not in ['PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED']:
            return {"status": "error", "message": "Invalid status"}, 400
    if 'maid_id' in data:
        try:
            data['maid_id'] = int(data['maid_id'])
        except ValueError:
            return {"status": "error", "message": "Invalid maid ID"}, 400
    
    if 'payment' in data:
        try:
            data['payment'] = float(data['payment'])
            if data['payment'] < 0:
                return {"status": "error", "message": "Payment cannot be negative"}, 400
        except ValueError:
            return {"status": "error", "message": "Invalid payment amount"}, 400
    
    if 'duration' in data:
        try:
            data['duration'] = int(data['duration'])
            if data['duration'] < 0:
                return {"status": "error", "message": "Duration cannot be negative"}, 400
        except ValueError:
            return {"status": "error", "message": "Invalid duration"}, 400
    
    if 'status' in data and data['status'] == 'CONFIRMED':
        data['payment_date'] = 'CURRENT_TIMESTAMP'
    
    success, error = update_booking(booking_id, data)
    
    if not success:
        return {"status": "error", "message": error}, 400
    
    return {"status": "success", "message": "Booking updated successfully"}, 200

# get all booking for admin
def get_booking_history_service(booking_id):
    bookings, error = get_booking_history(booking_id)
    if error:
        return {"status": "error", "message": error}, 400
    return {"status": "success", "bookings": bookings}, 200