from app.extensions import db

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usertask_id = db.Column(db.Integer, db.ForeignKey('user_task.id'))
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    points = db.Column(db.Integer)
    status = db.Column(db.String(80))
    user = db.relationship('User', backref='reward', uselist=False)
    usertask = db.relationship('UserTask', backref='reward', uselist=False)


    @classmethod
    def add(cls, usertask, status):
        reward = cls(usertask_id=usertask.id, user_id=usertask.user_id, points=usertask.task.points, status=status)
        db.session.add(reward)            
        db.session.commit()
        return reward
    

    def claim(self):
        self.status = 'Claimed'
        self.user.add_point(self.task.points)
        self.user.block_points(-self.task.points)
        self.usertask.task.get_admin().block_points(-self.task.points)
        db.session.commit()