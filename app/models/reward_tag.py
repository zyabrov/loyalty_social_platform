from app.extensions import db

reward_tag = db.Table(
    'reward_tag',
    db.Column('reward_id', db.Integer, db.ForeignKey('reward.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)