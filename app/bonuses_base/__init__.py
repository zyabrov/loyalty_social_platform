from flask import Blueprint
bp = Blueprint('bonuses_base', __name__)


from app.bonuses_base import routes

