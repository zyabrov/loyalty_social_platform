from flask import Blueprint
bp = Blueprint('certificates', __name__)


from app.certificates import routes

