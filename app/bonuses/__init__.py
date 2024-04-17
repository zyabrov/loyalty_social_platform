from flask import Blueprint
bp = Blueprint('bonuses', __name__, url_prefix='/bonuses', template_folder='templates')


from app.bonuses import routes

