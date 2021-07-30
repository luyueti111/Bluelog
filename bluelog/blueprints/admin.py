from flask import Blueprint

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/test')
def login():
    return "this is admin's test"
