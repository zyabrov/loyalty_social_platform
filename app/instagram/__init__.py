from flask import Blueprint

bp = Blueprint('instagram', __name__, url_prefix='/instagram', template_folder='templates')


from app.instagram import routes