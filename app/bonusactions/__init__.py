from flask import Blueprint
bp = Blueprint('bonusactions', __name__, url_prefix='/bonusactions', template_folder='templates')


from app.bonusactions import routes

