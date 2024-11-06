from flask import Blueprint

bp = Blueprint('conditions', __name__, url_prefix='tasks/conditions', template_folder='templates')


from app.conditions import routes
