from app.extensions import db

class RewardAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'), nullable=False)

    def __repr__(self):
        return '<RewardAction %r>' % self.name
    
    def serialize(self):
        return {k: getattr(self, k) for k in self.__table__.columns.keys()}
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get(id):
        return RewardAction.query.get(id)