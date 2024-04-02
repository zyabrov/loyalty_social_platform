from app.extensions import db

user_tag = db.Table(
    'user_tag',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)