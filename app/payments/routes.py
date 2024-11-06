from flask import render_template, request, url_for, redirect, flash, send_from_directory
from app.payments import bp
from flask_login import login_required, login_user, current_user, logout_user
from app.extensions import login_manager


@bp.route('/new', methods=['GET', 'POST'])
def new_payment():
    pass