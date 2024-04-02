from app.extensions import db

bonusaction_tag = db.Table(
    'bonusaction_tag',
    db.Column('bonusaction_id', db.Integer, db.ForeignKey('bonus_action.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)