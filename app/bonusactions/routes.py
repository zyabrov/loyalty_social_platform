from flask import render_template, request, jsonify
from app.bonusactions import bp
from app import db
from app.models import BonusAction, Bonus, BonusBase, User, Company
from app.forms import NewBonusActionForm
from datetime import datetime
from flask_login import login_required



@bp.route('/')
@login_required
def all_bonusactions():
    print(BonusAction.query.all())
    for bonusaction in BonusAction.query.all():
        print(bonusaction.user_id)
    return render_template('bonusactions/index.html', bonusactions=BonusAction.query.all())


@bp.route('/<int:bonusaction_id>')
@login_required
def bonusaction(bonusaction_id):
    return render_template('bonusactions/bonusaction.html', bonusaction=BonusAction.query.get_or_404(bonusaction_id))


@bp.route('/new_bonusaction', methods=['GET', 'POST'])
@login_required
def new_bonusaction():
    form = NewBonusActionForm()
    if form.validate_on_submit():
        bonus = Bonus.get(form.bonus.data)
        user = User.get(form.user.data)
        bonusaction = BonusAction(
            name=f'{user.username} - {bonus.name}',
            date_created=datetime.now(),
            bonus_id=bonus.id,
            user_id=user.id,
            company_id = Company.get(form.company.data).id
            )
        db.session.add(bonusaction)
        db.session.commit()
        return render_template('bonusactions/index.html', bonusactions=BonusAction.query.all())
        
    return render_template('bonusactions/new_bonusaction.html', form=form)

@bp.route('/get_bonus', methods=['POST'])
def get_bonus():
    data = request.get_json()
    print('request data', data)
    user = User.get(data['user_id'])
    bonus = Bonus.get(data['bonus_id'])
    company = Company.get(data['company_id'])
    bonusaction = BonusAction(
        name=f'{user.username} - {bonus.name}',
        date_created=datetime.now(),
        bonus_id=bonus.id,
        user_id=user.id,
        company_id=company.id
    )
    db.session.add(bonusaction)
    db.session.commit()
    
    return jsonify({'success': True, 'data': bonusaction.serialize(), 'message': 'Bonus action created successfully'})

@bp.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    bonusaction = BonusAction.get(id)
    bonusaction.delete()
    return render_template('bonusactions/index.html', bonusactions=BonusAction.query.all())