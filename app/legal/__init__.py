from flask import Blueprint
bp = Blueprint('legal', __name__, url_prefix='/legal', template_folder='templates')


from app.legal import routes