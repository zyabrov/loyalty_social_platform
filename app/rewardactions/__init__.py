from flask import Blueprint
bp = Blueprint('rewardactions', __name__, url_prefix='/rewardactions', template_folder='templates')


from app.rewardactions import routes

