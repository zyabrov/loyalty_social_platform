from flask import flash, render_template, request, url_for, redirect, flash, current_app
from flask_login import login_required, current_user
import instaloader
from app.users import bp
from datetime import datetime
from app.users.forms import AddPointsForm, AddInstagramForm

from app.users.models import User, SuperAdmin
from app.admins.models import Admin

import os


@bp.route('/')
@login_required
def all_users():
    return render_template('users/index.html', users=User.query.all())


@bp.route('/<int:user_id>')
@login_required
def user(user_id):
    return render_template('users/user.html', user=User.query.get(user_id))

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)



@bp.route('/add_points', methods=['GET', 'POST'])
@login_required
def add_points():

    form = AddPointsForm(request.form)
    
    if request.method == 'POST':
        print('add_points post request: ', request.form)
        if form.validate_on_submit():
            current_user.add_points(points=form.points_input.data, reason=form.reason.data)
            flash('Points has been added', 'message')
            return redirect(url_for('dashboard.dashboard'))
            
        else:
            return render_template('add_points_form.html', form=form)
    
    return render_template('add_points_form.html', form=form)


@bp.route('/add_instagram_username', methods=['GET', 'POST'])
@login_required
def add_instagram_username():
    form = AddInstagramForm(request.form)
    if form.user_id.data is None:
        form.user_id.data = current_user.id        

    if form.validate_on_submit():
        print('form data: ', form.data)
        user = User.query.get(int(form.user_id.data))
        if user:
            # user.update(instagram_username=form.instagram_username.data)
            user.save_instagram_profile(form.instagram_username.data)
            if user.instagram_page:
                flash('Instagram profile has been added successfully', 'message')
                return redirect(url_for('dashboard.dashboard'))
        else:
            form.error = 'User not found'

    return render_template('add_instagram_username_form.html', form=form)

@bp.route('/activate_tg_bot', methods=['GET', 'POST'])
@login_required
def activate_tg_bot():
    url = current_app.config['BOT_URL'] + '?start=' + str(current_user.id)
    return render_template('activate_tg_bot.html', url=url)



@bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    notifications = current_user.notifications
    return render_template('notifications.html', notifications=notifications, user=current_user)


@bp.route('/delete', methods=['GET'])
@login_required
def delete():
    user = User.query.get(current_user.id)
    user.delete()
    return redirect(url_for('dashboard.dashboard'))


@bp.route('/check_following', methods=['GET'])
@login_required
def check_following():
    user = User.query.get(current_user.id)
    if user.check_following(1):
        return 'true'
    else:
        return 'false'
    

@bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    from app.users.models import User
    user = User.add(
        name = 'Superadmin',
        email = 'zyabrov@gmail.com',
        password = 'Test123',
        user_type = 'superadmin',
        phone = '+380635408182',
    )
    admin = Admin.add(user.id)
    from app.shops.models import Shop
    shop = Shop.add(
        name = 'Rational Life',
        admin_id = admin.id,
        instagram_username = 'loyaltybots',
        logo_url = os.path.join(current_app.config['SHOPS_UPLOAD_DIR'], 'loyaltybots', 'logo.jpg'),
        phone = user.phone,
    )
    admin.update_current_shop(shop.id)
    return 'done'
    
