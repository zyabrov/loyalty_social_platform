from flask import Blueprint
bp = Blueprint('tasks', __name__, url_prefix='/tasks', template_folder='templates')


from app.tasks import routes

