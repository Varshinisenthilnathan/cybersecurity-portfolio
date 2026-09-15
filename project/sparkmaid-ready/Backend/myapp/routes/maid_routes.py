from flask import Flask, request,Blueprint
from myapp.utils.db_utils import create_maid_table
from myapp.service.maid_service import( register_maid,
                                       get_maid_by_id_service,
                                       get_all_maids_service,
                                       update_maid_service,
                                       delete_maid_service)
from myapp.utils.auth_decorators import role_required 

maid_bp = Blueprint('maid_bp', __name__)
create_maid_table()

# CREATE NEW MAID 
@maid_bp.route('/maid/register', methods=['POST'])
@role_required("admin")
def register_maid_route():
    data = request.get_json()
    return register_maid(data)

# retrivr maid details by id
@maid_bp.route('/maid/<int:maid_id>', methods=['GET'])
@role_required("admin", "customer")
def get_maid_by_id_route(maid_id):
    return get_maid_by_id_service(maid_id)

# reteive all maid
@maid_bp.route('/maid', methods=['GET'])
@role_required("admin", "customer")
def get_all_maids_route():
    availability_status = request.args.get('availability_status')
    gender = request.args.get('gender')
    service = request.args.get('service')
        
    filters = {
        'availability_status': availability_status,
        'gender': gender,
        'service': service
        }
        
    return  get_all_maids_service(filters)
# update maid
@maid_bp.route('/maid/<int:maid_id>', methods=['PUT'])
@role_required("admin") 
def update_maid_route(maid_id):
    data = request.get_json()  
    print(data)
    return update_maid_service(maid_id, data) 

# soft delete maid
@maid_bp.route('/maid/<int:maid_id>', methods=['DELETE'])
@role_required("admin")
def soft_delete_maid_route(maid_id):
    data = request.get_json(silent=True) or {}
    deleted_by = data.get("deleted_by", "system")
    return delete_maid_service(maid_id, deleted_by)

        