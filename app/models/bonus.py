from app.extensions import db

class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    points_value = db.Column(db.Integer)
    bonusbase_id = db.Column(db.Integer, db.ForeignKey('bonus_base.id'))    
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    bonusactions = db.relationship('BonusAction', backref='bonus', lazy='dynamic')
    conditions = db.relationship('Condition', secondary='bonus_condition', backref='bonuses')
    def __repr__(self):
        return '<Bonus %r>' % self.name
    
    @staticmethod
    def get(bonus_id):
        return Bonus.query.get(bonus_id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()