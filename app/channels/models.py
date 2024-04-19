from app.extensions import db


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    channel_id = db.Column(db.Integer)
    channelbase_id = db.Column(db.Integer, db.ForeignKey('channel_base.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    