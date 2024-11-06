from flask import Blueprint
bp = Blueprint('shops', __name__, url_prefix='/shops', template_folder='templates')


from app.shops import routes