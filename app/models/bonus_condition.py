from app.extensions import db

bonus_condition = db.Table(
    'bonus_condition',
    db.Column('bonus_id', db.Integer, db.ForeignKey('bonus.id'), primary_key=True),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True)
)