from app.legal import bp
from flask import request, current_app, url_for, render_template, redirect
from flask_login import login_required, current_user

@bp.route('/privacy', methods=['GET'])
def privacy_page():
    return render_template('privacy.html')