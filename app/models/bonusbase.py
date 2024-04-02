from app.extensions import db

class BonusBase(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    base_amount = db.Column(db.Integer)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))    

    bonuses = db.relationship('Bonus', backref='bonusbase', lazy=True)
    conditions = db.relationship('Condition', secondary='bonusbase_condition', backref='bonusbase', lazy=True)
    
    def __repr__(self):
        return '<BonusBase {}>'.format(self.name)
    
    @staticmethod
    def get(id):
        return BonusBase.query.get(id)