from app.extensions import db


bonus_tag = db.Table(
    'bonus_tags',
    db.Column('bonus_id', db.Integer, db.ForeignKey('bonus.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


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