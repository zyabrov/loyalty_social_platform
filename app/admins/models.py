from app.extensions import db
from app.shops.models import Shop



class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    blocked_points = db.Column(db.Integer, default=0)
    current_shop_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='admin', uselist=False)
    current_shop = None


    @property
    def current_shop(self):
        if not hasattr(self, '_current_shop'):
            self._current_shop = Shop.query.get(self.current_shop_id)
        return self._current_shop


    @classmethod
    def add(cls, user_id):
        admin = cls(user_id=user_id)
        db.session.add(admin)
        db.session.commit()
        return admin
    
    def update_current_shop(self, shop_id):
        self.current_shop_id = shop_id
        db.session.commit()


    def block_points(self, points, reason, task_id=None):
        if points < 0:
            name = 'Unblocked points'
        else:
            name = 'Blocked points'

        from app.actions.models import PointsAction
        PointsAction.add(
            points=points, 
            user_id=self.id, 
            name=name, 
            reason=reason, 
            task_id=task_id)
        self.blocked_points += points
        db.session.commit()


    @classmethod
    def get_by_user_id(cls, user_id):
        return Admin.query.filter_by(user_id=user_id).first()
    

    @classmethod
    def get_by_shop_id(cls, shop_id):
        return Admin.query.filter_by(current_shop_id=shop_id).first()
    
    def submit_reward(self, reward_id):
        from app.rewards.models import Reward
        reward = Reward.query.get(reward_id)
        reward.status = 'Submitted'
        db.session.commit()


    def add_points(self, points, reason, from_user_id=None, task_id=None):
        self.user.add_points(points, reason, from_user_id, task_id)



class Superadmin(Admin):
    def __init__(self, **kwargs):
        super(Superadmin, self).__init__(**kwargs)
        self.user_type = 'superadmin'
        self.user_id = 4


