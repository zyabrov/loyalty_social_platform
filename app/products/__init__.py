from flask import Blueprint

bp = Blueprint('products', __name__, url_prefix='/products', template_folder='templates')