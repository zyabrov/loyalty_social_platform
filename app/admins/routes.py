from app.admins import bp
from app import db
from app.admins.models import Admin
from flask_login import login_required, current_user
from flask import render_template, url_for, request


@bp.route('/')
def index():
    admins = Admin.query.all()
    admins_list = []
    for admin in admins:
        admins_list.append(admin.id)
    return admins_list

@bp.route('/edit_profile', methods=['GET'])
@login_required
def edit_profile():
    admin = Admin.query.get(current_user)
    return render_template('admin_card.html', admin=admin)
    


@bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    db.session.add(Admin())
    db.session.commit()
    return 'Admin added'


@bp.route('/add_points/<int:admin_id>/<int:points>', methods=['GET'])
def add_points(admin_id, points):
    admin = Admin.query.get(admin_id)
    reason = request.args.get('reason', None)
    task_id = request.args.get('task_id', None)
    from_user_id = request.args.get('from_user_id', None)
    if admin:
        from app.users.models import User
        user = User.query.get(admin.user_id)
        user.add_points(points, reason, from_user_id=None, task_id=None)
    return 'Points added'


@bp.route('/buy_points', methods=['GET'])
def buy_points():
    return render_template('buy_points.html')