from flask import Blueprint
bp = Blueprint('bonuses', __name__)


from app.bonuses import routes

