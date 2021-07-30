from flask import Blueprint

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/test')
def login():
    return "this is blog's test"
