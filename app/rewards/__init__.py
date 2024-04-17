from flask import Blueprint
bp = Blueprint('rewards', __name__, url_prefix='/rewards', template_folder='templates')


from app.rewards import routes

