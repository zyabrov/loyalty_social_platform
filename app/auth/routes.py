from datetime import datetime
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user, login_user
from app.auth import bp
from app import db
from app.users.models import User
from app.auth.forms import LoginForm, SignUpForm


@bp.route('/', methods=['GET', 'POST'])
def index():

    return redirect(url_for('auth.login'))


@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, registered=datetime.now(), role='user')
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.index'))
    
    return render_template('sign_up.html', form=form)



@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)

    if form.validate_on_submit():
        print('\n\n--------------\n')
        print('user:', User.query.filter_by(username=form.username.data).first())

        user = User.query.filter_by(username=form.username.data).first()
        print('User: ', user)

        if user is None:    
            return render_template('login.html', form=form, error='Invalid username or password')
        
        else:
            print('User exists: ', user)

        login_user(user)

        return redirect(url_for('main.index'))
    
    return render_template('login.html', form=form)

    