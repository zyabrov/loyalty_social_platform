from flask import render_template
from app.instagram import bp

@bp.route('/', methods=['GET'])
