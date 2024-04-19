from flask import render_template
from app.rewards import bp
from app import db
from app.rewards.models import Reward
from app.rewards.forms import NewRewardForm


@bp.route('/', methods=['GET'])
def all_rewards():
    return render_template('rewards/index.html', rewards=Reward.query.all())


@bp.route('/<reward_id>', methods=['GET'])
def reward(reward_id):
    return render_template('rewards/reward.html', reward=Reward.query.get(reward_id))

@bp.route('/new_reward', methods=['GET', 'POST'])
def new_reward():
    form = NewRewardForm()

    if form.validate_on_submit():
        reward = Reward(
            name='Certificate ' + str(form.points_costs.data),
            points_costs = form.points_costs.data,
            description=form.description.data,
        )
        db.session.add(reward)
        db.session.commit()
        return render_template('rewards/index.html', rewards=Reward.query.all())
    
    return render_template('rewards/new_reward.html', form=form)

@bp.route('/delete/<reward_id>', methods=['GET', 'POST'])
def delete_reward(reward_id):
    reward = Reward.get(reward_id)
    reward.delete()
    return render_template('rewards/index.html', rewards=Reward.query.all())