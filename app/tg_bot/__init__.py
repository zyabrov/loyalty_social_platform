from flask.blueprints import Blueprint
bp = Blueprint('tg_bot', __name__)

from app.tg_bot import routes