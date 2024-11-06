from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from app.dashboard import bp
from app.admins.models import Admin
from app.users.models import User

 

@bp.route('/')
@login_required
def dashboard():
    user_id = current_user.id
    user = User.query.get(user_id)
    if user.name != 'Superadmin':
        if user.telegram_id is None:
                return redirect(url_for('users.activate_tg_bot'))
        else:
            if user.admin:
                admin = Admin.get_by_user_id(user.id)
                if admin.current_shop:
                    return render_template('admin_dashboard.html', admin=admin)
            else:
                if user.instagram_submitted is not True:
                    return redirect(url_for('users.add_instagram_username'))

            return render_template('user_dashboard.html', user=user, add_instagram_username_form_url=url_for('users.add_instagram_username', _external=True, activate_telegram_bot=url_for('users.activate_tg_bot', _external=True)))
    else:
         admin = Admin.get_by_user_id(user.id)
         return render_template('admin_dashboard.html', admin=admin)
    

