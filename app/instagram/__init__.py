from flask import Blueprint
bp = Blueprint('instagram', __name__)


from app.instagram import routes

