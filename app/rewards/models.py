from app.extensions import db


reward_tag = db.Table(
    'reward_tag',
    db.Column('reward_id', db.Integer, db.ForeignKey('reward.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    points_costs = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    
    tags = db.relationship('Tag', secondary='reward_tag', backref='rewards', lazy=True)
    rewardactions = db.relationship('RewardAction', backref='reward', lazy=True)

    def __repr__(self):
        return '<Reward %r>' % self.name
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get(reward_id):
        return Reward.query.get(reward_id)