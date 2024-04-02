from app.extensions import db


bonusbase_condition = db.Table(
    'bonusbase_condition',
    db.Column('bonusbase_id', db.Integer, db.ForeignKey('bonus_base.id'), primary_key=True),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True)
)