from app.extensions import db
from datetime import datetime


class Certificate(db.Model):
    __tablename__ = "certificate"
    id = db.Column(db.Integer, primary_key=True)
    cert_code = db.Column(db.String(255))
    activated_date = db.Column(db.DateTime)
    used_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    points = db.Column(db.Integer)

    rewardaction = db.relationship("RewardAction", backref="certificate", uselist=False)

    def __repr__(self):
        return "<Certificate %r>" % self.id
    
    @staticmethod
    def create(user_id, company_id, points,**kwargs):

        certificate = Certificate(**kwargs)
        certificate.user_id = user_id
        certificate.company_id = company_id
        certificate.points = points
        certificate.cert_code = generate_cert_code()
        certificate.activated_date = datetime.now()
        certificate.status = 1
        db.session.add(certificate)
        db.session.commit()
        
        return certificate
        
    def serialize(self):
        return {k: getattr(self, k) for k in self.__table__.columns.keys()}
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
def generate_cert_code():
    import string
    import random
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))