from flask import request,Blueprint
from myapp.utils.db_utils import create_admin_table
from myapp.service.admin_service import register_admin,get_all_admins_service,update_admin_service
from myapp.utils.auth_decorators import role_required 

admin_bp = Blueprint('admin_bp', __name__)

create_admin_table()
# create admin
@admin_bp.route("/admin/register", methods=["POST"])
#@role_required("admin") 
def register_admin_route():
        data = request.get_json()
        return register_admin(data)

# retive he admin details
@admin_bp.route('/admins', methods=['GET'])
@role_required("admin") 
def get_all_admins_route():
    return get_all_admins_service()

# update the admin details
@admin_bp.route('/admins/<int:admin_id>', methods=['PUT'])
@role_required("admin") 
def update_admin_route(admin_id):
    update_data = request.get_json()
    return update_admin_service(admin_id, update_data)