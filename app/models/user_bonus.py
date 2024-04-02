from app.extensions import db

user_bonus = db.Table(
    'user_bonus',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('bonus_id', db.Integer, db.ForeignKey('bonus.id'))
)