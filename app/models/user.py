from app.extensions import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.Integer, index=True, unique=True)
    registered = db.Column(db.DateTime)
    password_hash = db.Column(db.String(128))

    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    bonuses = db.relationship('Bonus', secondary='user_bonus', backref='users', lazy='dynamic')
    bonusactions = db.relationship('BonusAction', backref='user', lazy='dynamic')
    certificates = db.relationship('Certificate', backref='user', lazy='dynamic')
    rewardactions = db.relationship('RewardAction', backref='user', lazy='dynamic')
    
    tags = db.relationship('Tag', secondary='user_tag', backref='users', lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    @staticmethod
    def check_password(self, password):
        # TODO: Add password hashing
        if password == self.password_hash:
            return True
        else:
            return False
        
    def set_password(self, password):
        self.password_hash = password

    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))

    @property
    def total_points(self):
        bonus_points = sum([bonusaction.bonus.points_value for bonusaction in self.bonusactions])
        reward_points = sum([rewardaction.reward.points_costs for rewardaction in self.rewardactions])
        return bonus_points - reward_points    
    
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

