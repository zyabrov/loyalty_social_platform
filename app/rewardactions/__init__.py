from flask import Blueprint
bp = Blueprint('rewardactions', __name__)


from app.rewardactions import routes

