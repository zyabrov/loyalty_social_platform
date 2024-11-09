from flask import render_template, request, url_for, redirect, flash, send_from_directory
from app.main import bp
from flask_login import login_required, login_user, current_user, logout_user
from app.extensions import login_manager
from app import db
from app.users.forms import LoginForm, SignUpForm
from app.users.models import User


@bp.route('/', methods=['GET'])
def index():
    
    if login_user(current_user):
        return redirect(url_for('dashboard.dashboard'))
    else:
        referrer_id = None
        if request.args.get('ref_id'):
            referrer_id = request.args.get('ref_id')
        return render_template('index.html', referrer_id=referrer_id)
            

@bp.route('/create_tables')
def create_tables():
    db.drop_all()
    db.create_all()
    from app.tasks.models import BaseTask
    BaseTask.add_base_tasks()
    from app.shops.models import Category
    Category.add_base_categories()
    from app.users.routes import add_admin
    add_admin()
    return 'Tables created'

@bp.route('/new_tables')
def new_tables():
    db.create_all()
    return 'Tables created'



@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('main.index'))

def signup(user_type, referrer_id=None):
    from app.users.models import User
    form = SignUpForm(request.form)
    form.user_type.process_data(user_type)
    if referrer_id:
        form.referrer_id.process_data(referrer_id)


    if request.method == 'POST':
        if form.validate_on_submit():
            print('user phone: ', form.phone.data)
            user = User.query.filter_by(phone=form.phone.data).first()
            if user:
                # User already exists, redirect to login
                flash('User already exists. Please login instead.')
                return redirect(url_for('login'))
            else:
                # Create new user

                user = User.add(
                    name=form.name.data,
                    phone=form.phone.data,
                    referrer_id=form.referrer_id.data,
                    password=form.password.data,
                    email=form.email.data,
                    user_type=form.user_type.data,
                    
                )
                login_user(user)

                if form.user_type.data == 'admin':
                    from app.admins.models import Admin
                    Admin.add(user_id=user.id)
                    
                return redirect(url_for('dashboard.dashboard'))
        
        else: 
            flash('Please correct the errors in the form')
            print(form.errors)

    return render_template('signup.html', form=form)


@bp.route('/user_signup', methods=['GET'])
def user_signup(referrer_id=None):
    referrer_id=referrer_id
    if request.args.get('referrer_id'):
        referrer_id = request.args.get('referrer_id')
    return signup(user_type='user', referrer_id=referrer_id)


@bp.route('/admin_signup', methods=['GET'])
def admin_signup(referrer_id=None):
    referrer_id=referrer_id
    if request.args.get('referrer_id'):
        referrer_id = request.args.get('referrer_id')
    return signup(user_type='admin', referrer_id=referrer_id)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        from app.users.models import User
        if form.phone.data:
            print('user phone: ', form.phone.data)
            user = User.query.filter_by(phone=form.phone.data).first()
        else:
            if form.email.data:
                user = User.query.filter_by(email=form.email.data).first()
        print('User: ', user)

        if user:
            print('User exists: ', user)
            if user.check_password(form.password.data) == True:
                login_user(user)
                return redirect(url_for('dashboard.dashboard'))
            else:
                return render_template('login.html', form=form, error='Invalid username or password')
        
        else:
            print('User does not exist: ', user)
            return redirect(url_for('main.signup'))
    
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))




                
    

@bp.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('help.html')


@bp.route('/close_form', methods=['GET'])
def close_form():
    return render_template('pop-up.html')



