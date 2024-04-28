from flask import render_template
from app.users import bp
from app import db
from app.users.models import User
from app.forms import NewUserForm
from datetime import datetime
from flask_login import login_required, current_user


@bp.route('/', methods=['GET'])
@login_required
def all_users():
    user = current_user
    print('user: ', user)

    return render_template('users.html', users=User.query.all())

@bp.route('/', methods=['GET', 'POST'])



@bp.route('/<int:user_id>')
def user(user_id):
    return render_template('user.html', user=User.query.get(user_id))

