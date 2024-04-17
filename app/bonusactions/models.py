from app.extensions import db

bonusaction_tag = db.Table(
    'bonusaction_tag',
    db.Column('bonusaction_id', db.Integer, db.ForeignKey('bonus_action.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class BonusAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    bonus_id = db.Column(db.Integer, db.ForeignKey('bonus.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    tags = db.relationship('Tag', secondary='bonusaction_tag', backref='bonusactions')
    
    def __repr__(self):
        return '<BonusAction %r>' % self.name
    
    def serialize(self):
        return {k: getattr(self, k) for k in self.__table__.columns.keys()}
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get(id):
        return BonusAction.query.get(id)