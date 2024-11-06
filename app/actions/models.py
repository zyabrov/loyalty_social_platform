from app.extensions import db
from app.rewards.models import Reward
    
class TasksActions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'))

    user = db.relationship('User', backref='tasks_actions')
    task = db.relationship('Task', backref='tasks_actions')
    reward = db.relationship(Reward, backref='tasks_actions')


    @classmethod
    def add(cls, user_id, task_id, name):
        new_action = cls(user_id=user_id, task_id=task_id, created_at=db.func.now(), name=name)
        db.session.add(new_action)
        db.session.commit()
        return new_action



class PointsAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    reason = db.Column(db.String(80), unique=False, nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    user = db.relationship('User', backref='pointsactions', foreign_keys='PointsAction.user_id')
    from_user = db.relationship('User', backref='pointsactions_from_user', foreign_keys='PointsAction.from_user_id')


    @classmethod
    def add(cls, points, user_id, name, reason, from_user_id=None, task_id=None):
        new_points_action = cls(points=points, user_id=user_id, created_at=db.func.now(), name=name, reason=reason, from_user_id=from_user_id, task_id=task_id)
        db.session.add(new_points_action)
        db.session.commit()
        return new_points_action

