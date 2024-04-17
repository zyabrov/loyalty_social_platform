from app.extensions import db

class ChannelBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    channels = db.relationship('Channel', backref='channelbase', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Channel %r>' % self.name