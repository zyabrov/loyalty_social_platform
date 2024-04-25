from flask import render_template
from app.admins import bp
from app import db
from app.users.models import User
from app.admins.models import Admin
from app.forms import NewUserForm
from datetime import datetime


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('dashboard.html')


@bp.route('/users', methods=['GET', 'POST'])
def all_users():
    admin = Admin.query.get(1)
    users = admin.get_company_users()
    print('\n\n-----------------')
    print('users: ', users)
    return render_template('users.html', users=users)


@bp.route('/bonusactions', methods=['GET', 'POST'])
def all_bonusactions():
    admin = Admin.query.get(1)
    bonusactions = admin.get_company_bonusactions()
    print('\n\n-----------------')
    for ba in bonusactions:
        print('bonusaction: ', ba)
    return render_template('bonusactions.html', bonusactions=bonusactions)


@bp.route('/rewardactions', methods=['GET', 'POST'])
def all_rewardactions():
    admin = Admin.query.get(1)
    rewardactions = admin.get_company_rewardactions()
    print('\n\n-----------------')
    for ra in rewardactions:
        print('rewardaction: ', ra)
    return render_template('rewardactions.html', rewardactions=rewardactions)


@bp.route('/certificates', methods=['GET', 'POST'])
def all_certificates():
    admin = Admin.query.get(1)
    certificates = admin.get_company_certificates()
    print('\n\n-----------------')
    for cert in certificates:
        print('certificate: ', cert)
    return render_template('certificates.html', certificates=certificates)