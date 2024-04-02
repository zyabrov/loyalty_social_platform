from flask import render_template
from app.main import bp
from app import db
from app.forms import LoginForm, SignUpForm
from app.models import User
from flask_login import login_required, login_user


@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/create_tables')
def create_tables():
    db.drop_all()
    db.create_all()
    return 'Tables created'

@bp.route('/new_tables')
def new_tables():
    db.create_all()
    return 'Tables created'


@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        print('\n\n--------------\n')
        print('user:', User.query.filter_by(username=form.username.data).first())
        
        user = User.get_by_username(form.username.data)
        print('User: ', user)

        if user is None:
            return render_template('login.html', form=form, error='Invalid username or password')
                
        else:
            print('User exists: ', user)

        login_user(user)

        return render_template('index.html')
    
    return render_template('login.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return render_template('index.html')
    
    return render_template('signup.html', form=form)