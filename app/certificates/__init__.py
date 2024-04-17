from flask import Blueprint
bp = Blueprint('certificates', __name__, url_prefix='/certificates', template_folder='templates')


from app.certificates import routes

