from flask import Blueprint
bp = Blueprint('admins', __name__, url_prefix='/admins', template_folder='templates')


from app.admins import routes