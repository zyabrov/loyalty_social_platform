from flask import render_template, request, jsonify
from app.bonuses import bp
from app import db
from app.bonuses.models import Bonus
from app.bonuses_base.models import BonusBase
from app.bonuses.forms import NewBonusForm


@bp.route('/', methods=['GET'])
def all_bonuses():
    return render_template('bonuses.html', bonuses=Bonus.query.all())


@bp.route('/<bonus_id>', methods=['GET'])
def bonus(bonus_id):
    return render_template('bonus.html', bonus=Bonus.query.get(bonus_id))

@bp.route('/new_bonus', methods=['GET', 'POST'])
def new_bonus():
    form = NewBonusForm()

    if form.validate_on_submit():
        print(form.bonus_base_id.data)
        bonus_base = BonusBase.query.get(form.bonus_base_id.data)
        bonus = Bonus(
            description=form.description.data,
            points_value=form.points_value.data,
            bonusbase_id=bonus_base.id,
            name=bonus_base.name
        )
        db.session.add(bonus)
        db.session.commit()
        return render_template('bonuses/bonuses.html', bonuses=Bonus.query.all())
    
    return render_template('bonuses/new_bonus.html', form=form)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    bonus = Bonus.query.get(id)
    db.session.delete(bonus)
    db.session.commit()
    return render_template('bonuses/bonuses.html', bonuses=Bonus.query.all())


@bp.route('/basebonus_selected', methods=['POST'])
def basebonus_selected():
    id = int(request.form['bonus_base_id'])
    basebonus = BonusBase.get(id)
    form = NewBonusForm(request.form)
    form.points_value.data = basebonus.base_amount
    print('basebonus selected: ', basebonus)
    print('basebonus base_amount: ', basebonus.base_amount)
    return jsonify({'success': True, 'message': 'Points value updated'})