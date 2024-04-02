from app.extensions import db

company_location = db.Table(
    'company_location',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
)