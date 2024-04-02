from app.extensions import db

user_reward = db.Table(
    'user_reward',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('reward_id', db.Integer, db.ForeignKey('reward.id'), primary_key=True)
)