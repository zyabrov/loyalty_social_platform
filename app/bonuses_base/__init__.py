from flask import Blueprint
bp = Blueprint('bonuses_base', __name__, url_prefix='/bonuses_base', template_folder='templates')


from app.bonuses_base import routes

