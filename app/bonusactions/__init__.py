from flask import Blueprint
bp = Blueprint('bonusactions', __name__)


from app.bonusactions import routes

