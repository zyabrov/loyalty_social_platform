from app.extensions import db

bonus_tag = db.Table(
    'bonus_tags',
    db.Column('bonus_id', db.Integer, db.ForeignKey('bonus.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)