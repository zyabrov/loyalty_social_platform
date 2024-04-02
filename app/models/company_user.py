from app.extensions import db

company_user = db.Table(
    'company_user',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)