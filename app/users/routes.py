from flask import render_template
from app.users import bp
from app import db
from app.models import User
from app.forms import NewUserForm
from datetime import datetime


@bp.route('/')
def all_users():
    return render_template('users/index.html', users=User.query.all())


@bp.route('/<int:user_id>')
def user(user_id):
    return render_template('users/user.html', user=User.query.get(user_id))

@bp.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = NewUserForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            phone = form.phone.data,
            registered = datetime(),
        )
        db.session.add(user)
        db.session.commit()
        return render_template('users/index.html', users=User.query.all())
    
    return render_template('users/new_user.html', form=form)