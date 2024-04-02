from app.extensions import db

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128))

    def __repr__(self):
        return '<Condition {}>'.format(self.name)