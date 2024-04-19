from flask import render_template, request, jsonify, url_for
from app.rewardactions import bp
from app import db
from app.users.models import User
from app.rewards.models import Reward
from app.rewardactions.models import RewardAction
from app.companies.models import Company
from app.rewardactions.forms import NewRewardActionForm
from datetime import datetime
from flask_login import login_required
from app.extensions import requests

base_dir = 'http://localhost:5000'

@bp.route('/')
@login_required
def all_rewardactions():
    print(RewardAction.query.all())        
    return render_template('rewardactions/index.html', rewardactions=RewardAction.query.all())


@bp.route('/<int:rewardaction_id>')
@login_required
def re(rewardaction_id):
    return render_template('rewardactions/rewardaction.html', rewardactions=RewardAction.query.get_or_404(rewardaction_id))


@bp.route('/new_rewardaction', methods=['GET', 'POST'])
@login_required
def new_rewardaction():
    form = NewRewardActionForm()

    if form.validate_on_submit():
        name="New Reward"
        rewardaction = RewardAction(
            name=name,
            date_created=datetime.now(),
            reward_id=form.reward.data,
            user_id=form.user.data
            )
        db.session.add(rewardaction)
        db.session.commit()
        return render_template('rewardactions/index.html', rewardactions=RewardAction.query.all())
        
    return render_template('rewardactions/new_rewardaction.html', form=form)

@bp.route('/get_reward', methods=['POST'])
def get_reward():
    data = request.get_json()
    reward = Reward.query.get_or_404(data['reward_id'])
    user = User.get(data['user_id'])
    company = Company.get(data['company_id'])

    if user.total_points and int(reward.points_costs) < int(user.total_points):
        # Make a POST request to the new_certificate endpoint
        certificate_data = {
            "user_id": user.id,
            "company_id": company.id,
            "points": reward.points_costs
        }
        
        
        certificate_response = requests.post(base_dir + '/certificates/new_certificate', json=certificate_data)
        print(certificate_response.json())

        if certificate_response.status_code == 200:
            rewardaction = RewardAction(
                    name=f'{user.username} - {reward.name}',
                    date_created=datetime.now(),
                    reward_id=reward.id,
                    user_id=user.id,
                    certificate_id=certificate_response.json()['certificate']['id']
                    )
            db.session.add(rewardaction)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Certificate generated', 'data': rewardaction.serialize()})
        else:
            return jsonify({'success': False, 'message': 'Failed to generate certificate'})
        
    
    return jsonify({'success': False, 'message': 'Insufficient points or invalid reward'})


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    rewardaction = RewardAction.get(id)
    rewardaction.delete()
    return render_template('rewardactions/index.html', rewardactions=RewardAction.query.all())