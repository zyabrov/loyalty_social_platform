from app.extensions import db
from app.companies.models import Company

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
      
      
    def get_company_data(self):
        return Company.query.get(self.company_id)
    
    def get_company_users(self):
        return self.get_company_data().users
    
    def get_company_bonusactions(self):
        return self.get_company_data().bonusactions
    
    def get_company_rewardactions(self):
        return self.get_company_data().rewardactions
    
    def get_company_certificates(self):
        return self.get_company_data().certificates
