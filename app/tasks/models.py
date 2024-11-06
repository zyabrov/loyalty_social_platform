from app.extensions import db
from app.conditions.models import Condition
from app.users.models import User
from app.instagram.models import InstagramPost, Comment, InstagramPage

tasks = [{
        'name': 'Write a comment/feedback to Instagram post',
        'type': 'Comment',
        'channel': 'Instagram',
    }, {
        'name': 'Post a story on Instagram with @mention',
        'type': 'Mention',
        'channel': 'Instagram',
    }
    , {
        'name': 'Take a quiz',
        'type': 'QUIZ',
        'channel': 'App',
    }, {
        'name': 'Write a feedback on Google Maps',
        'type': 'Comment',
        'channel': 'Google Maps',
    }, {
        'name': 'Send a photo or video',
        'type': 'Send media',
        'channel': 'App',
    }, {
        'name': 'Write a feedback on website',
        'type': 'Comment',
        'channel': 'Website',
    }]

class BaseTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(80))
    channel = db.Column(db.String(80))
    
    @classmethod
    def add_task(cls, name, type, channel):
        task = BaseTask(name=name, type=type, channel=channel)
        db.session.add(task)
        db.session.commit()
        return cls
    
    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def add_base_tasks(cls):
        for task in tasks:
            cls.add_task(task['name'], task['type'], task['channel'])
    

tasks_conditions = db.Table('tasks_conditions',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True)
)

tasks_tags = db.Table('tasks_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

tasks_posts = db.Table('tasks_posts',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('instagram_post.id'), primary_key=True)
)



class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    points = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    basetask_id = db.Column(db.Integer, db.ForeignKey('base_task.id'))
    max_rewards = db.Column(db.Integer)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    total_points = db.Column(db.Integer)
    onetime = db.Column(db.Boolean)
    repeat_delay_hours = db.Column(db.Integer)
    repeat_max_times = db.Column(db.Integer)
    target_url = db.Column(db.String(80))
    status = db.Column(db.String(80))
    checking_type = db.Column(db.String(80))
    ai_conditions = db.Column(db.Text)
    only_followers = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    
    conditions = db.relationship('Condition', secondary=tasks_conditions, backref='tasks')
    shop = db.relationship('Shop', backref='tasks', uselist=False)
    basetask = db.relationship('BaseTask', backref='task', uselist=False)
    tags = db.relationship('Tag', secondary=tasks_tags, backref='tasks')
    posts = db.relationship('InstagramPost', secondary=tasks_posts, backref='tasks')


    def __repr__(self):
        return '<Task %r>' % self.name
    
    @staticmethod
    def get(task_id):
        return Task.query.get(task_id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def add(cls, basetask_id, name, points, max_rewards, total_points, shop_id, only_followers, onetime, checking_type, five_words, description=None, ai_conditions=None, repeat_delay_hours=None, repeat_max_times=None, target_url=None, posts:list[InstagramPost]=None):
        conditions = []
        if only_followers == True:
            conditions.append('Only followers')
        if onetime == True:
            conditions.append('Onetime')
        if five_words == True:
            conditions.append('Minimun 5 words')
        price = 0
        print('shop_id: ', shop_id)
        if shop_id != '1':
            price = points*0.3
        task = Task(
            basetask_id = basetask_id,
            name = name,
            points = points,
            max_rewards = max_rewards,
            total_points = total_points,
            shop_id=shop_id,
            onetime=onetime,
            repeat_delay_hours=repeat_delay_hours,
            repeat_max_times=repeat_max_times,
            target_url=target_url,
            only_followers=only_followers,
            checking_type=checking_type,
            ai_conditions=ai_conditions,
            status = 'New',
            price = price,
            description = description
            )
        db.session.add(task)
        if posts:
            print('posts: ', posts)
            from app.instagram.models import InstagramPost
            for post in posts:
                task.posts.append(post)
            print('task posts: ', task.posts)
        for item in conditions:
            from app.conditions.models import Condition
            condition = Condition.get_by_name(item)
            if condition:
                task.conditions.append(condition)
            else:
                condition = Condition.add(item)
                task.conditions.append(condition)
        db.session.commit()
        return task
    

    def check_conditions(self, user: User, usertask=None):
        responses = []
        for condition in self.conditions:
            condition_response = condition.check(self, user, usertask)
            print('condition response: ', condition_response)
            if condition_response is not True:
                responses.append(condition.name)
        print('response: ', responses)
        if len(responses) == 0:
            return True
        else:
            return responses


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def get_admin(self):
        from app.admins.models import Admin
        admin = Admin.query.get(self.shop.admin_id)
        return admin
    
    def start(self, user: User):
        usertask = UserTask.add(task=self, user=user)
        superadmin = User.query.get(1)
        superadmin.add_points(points=self.price, reason='Task started', task_id=self.id)
        from app.notifications.models import UserTaskStarted
        notification = UserTaskStarted(usertask)
        notification.send()


    def get_minimal_reward(cls, filter=None):
        minimal_reward = 0
        for task in Task.query.all():
            if task.points < minimal_reward:
                minimal_reward = task.points
        return minimal_reward
        
    @classmethod
    def get_max_reward(cls, filter=None):
        max_reward = 0
        for task in Task.query.all():
            if task.points > max_reward:
                max_reward = task.points
        return max_reward

    @classmethod
    def get_several_reward(cls, filter=None):
        total_points = 0
        for task in Task.query.all():
            total_points += task.points
        reward = total_points/len(Task.query.all())
        return reward

    


class UserTask(db.Model):
    __tablename__ = 'user_task'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    status = db.Column(db.String(80))
    date_started = db.Column(db.DateTime, nullable=False, default=db.func.now())
    date_finished = db.Column(db.DateTime)
    date_submitted = db.Column(db.DateTime)
    date_rewarded = db.Column(db.DateTime)
    date_refused = db.Column(db.DateTime)
    date_rejected = db.Column(db.DateTime)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    rejected_reason = db.Column(db.String(80))
    date_sent_to_check = db.Column(db.DateTime)

    user = db.relationship('User', backref='usertasks')
    task = db.relationship('Task', backref='usertasks')
    comment = db.relationship('Comment', backref='usertasks')

    @classmethod
    def add(cls, user, task):
        usertask = cls(user_id=user.id, task_id=task.id, status='Started')
        db.session.add(usertask)
        print('task points: ', int(task.points))
        user.add_points(points=-int(task.price), reason='Started task', task_id=task.id)
        user.block_points(points=int(task.points), reason='Started task', task_id=task.id)
        db.session.commit()
        return usertask
    

    def finish(self):
        self.date_finished = db.func.now()
        self.status = 'Finished'
        db.session.commit()

    def waiting_for_check(self):
        self.status = 'Waiting for admin submission'
        self.date_sent_to_check = db.func.now()
        db.session.commit()
        from app.notifications.models import UserTaskWaiting
        notification = UserTaskWaiting(self)
        notification.send()
        

    def submit(self):
        self.status = 'Submitted'
        self.date_submitted = db.func.now()
        self.task.get_admin().block_points(points=-self.task.points, reason='Submitted task', task_id=self.task.id)
        from app.rewards.models import Reward
        Reward.add(usertask=self, status='Pending')
        from app.notifications.models import UserTaskSubmitted
        notification = UserTaskSubmitted(self)
        notification.send()
        db.session.commit()


    def reject(self, rejected_reason):
        self.status = 'Rejected'
        self.rejected_reason = rejected_reason
        self.date_rejected = db.func.now()
        db.session.commit()
        from app.notifications.models import UserTaskRejected
        notification = UserTaskRejected(self)
        notification.send()


    def refuse(self):
        self.status = 'Refused'
        self.user.block_points(points=-self.task.points, reason='Refused task by User', task_id=self.task.id)
        self.date_refused = db.func.now()
        db.session.commit()


    def claim_reward(self):
        self.status = 'Claimed'
        self.user.add_points(points=self.task.points, reason='Claimed reward', task_id=self.task.id)
        self.user.block_points(points=-self.task.points, reason='Claimed reward', task_id=self.task.id)
        self.date_rewarded = db.func.now()
        db.session.commit()


    def add_comment(self, comment: Comment):

        self.comment_id = comment.id
        db.session.commit()
    

    def check_comment_ai(self, comment_text):
        from app.chatgpt import check_comment
        return check_comment(self.task.ai_conditions, comment_text)



    






