from flask import Blueprint

bp = Blueprint('actions', __name__, url_prefix='/actions', template_folder='templates')


from app.actions import routes