from flask import Blueprint
bp = Blueprint('main', __name__, url_prefix='/', template_folder='templates')


from app.main import routes

