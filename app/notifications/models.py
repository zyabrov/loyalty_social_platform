from app.extensions import db
from flask import url_for
from app.tasks.models import Task, UserTask
import asyncio
from app.tg_bot.routes import send_notification
from sqlalchemy import JSON
import json
from app.shops.models import Shop



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(80))
    date_sent = db.Column(db.DateTime, nullable=False, default=db.func.now())
    text = db.Column(db.Text)
    buttons = db.Column(JSON)
    image = db.Column(db.String(80))
    status = db.Column(db.String(80))
    usertask_id = db.Column(db.Integer, db.ForeignKey('user_task.id'))
    user = db.relationship('User', backref='notifications')
    usertask = db.relationship('UserTask', backref='notifications')
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    shop = db.relationship('Shop', backref='notifications')
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', backref='notifications')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'notification'
    }

    @classmethod
    def add(cls, user, type, text, buttons=None, image=None, usertask_id=None, shop_id=None):
        notification = Notification(user=user, type=type, date_sent=db.func.now(), text=text, buttons=buttons, image=image, status='New', usertask_id=usertask_id, shop_id=shop_id)
        db.session.add(notification)
        db.session.commit()
        return notification

    def __repr__(self):
        return '<Notification %r>' % self.type




class TaskAdded(Notification):

    def __init__(self, task: Task):
        db.session.add(self)
        super(TaskAdded, self).__init__()
        self.task = task
        self.user = task.shop.admin.user
        self.text = f'Task {self.task.name} added. Activate it for {self.task.total_points} points'
        buttons = [{'text': 'Activate now', 'url': url_for('tasks.activate', task_id=task.id)}]
        self.buttons = json.dumps(buttons)
        
    __mapper_args__ = {
        'polymorphic_identity': 'task_added'
    }

    def send(self):
        if self.user.telegram_id:
            buttons = json.loads(self.buttons)
            print('sending telegram notification')
            return send_notification(self.user.telegram_id, self.text, buttons)

class UserTaskStarted(Notification):

    def __init__(self, usertask: UserTask):
        db.session.add(self)  # Add the UserTaskStarted object to the session
        db.session.commit()
        super(UserTaskStarted, self).__init__()
        self.usertask = usertask
        self.user = usertask.user
        self.text = f'''You have started the task: 
{self.usertask.task.name}.
Complete it and get {self.usertask.task.points} points.'''
        buttons = [{'text': 'View details', 'url': url_for('tasks.usertask', usertask_id=usertask.id)}]
        self.buttons = json.dumps(buttons)

    def send(self):
        if self.user.telegram_id:
            buttons = json.loads(self.buttons)
            print('sending telegram notification')
            print('buttons: ', buttons)
            return send_notification(self.user.telegram_id, self.text, buttons)

    __mapper_args__ = {
        'polymorphic_identity': 'usertask_started'
    }

class UserTaskWaiting(Notification):

    def __init__(self, usertask: UserTask):
        db.session.add(self)  # Add the UserTaskWaiting object to the session
        db.session.commit()
        super(UserTaskWaiting, self).__init__()
        self.usertask = usertask
        self.user = usertask.task.shop.admin.user
        self.text = f'''User has finished the task. Check and confirm or reject it.'''
        buttons = [{'text': 'Task info', 'url': url_for('tasks.usertask', usertask_id=usertask.id)}]
        self.buttons = json.dumps(buttons)

    def send(self):
        if self.user.telegram_id:
            buttons = json.loads(self.buttons)
            print('sending telegram notification')
            return send_notification(self.user.telegram_id, self.text, buttons)

    __mapper_args__ = {
        'polymorphic_identity': 'usertask_waiting'
    }


class UserTaskSubmitted(Notification):

    def __init__(self, usertask: UserTask):
        db.session.add(self)  # Add the UserTaskSubmitted object to the session
        db.session.commit()
        super(UserTaskSubmitted, self).__init__()
        self.usertask = usertask
        self.user = usertask.user
        self.text = f'''Congratulations! You have completed the task: 
{self.usertask.task.name}.
You get {self.usertask.task.points} points.
Your points: {self.user.points}'''
        buttons = [{'text': 'Task info', 'url': url_for('tasks.usertask', usertask_id=usertask.id)}]
        self.buttons = json.dumps(buttons)

    def send(self):
        if self.user.telegram_id:
            buttons = json.loads(self.buttons)
            print('sending telegram notification')
            return send_notification(self.user.telegram_id, self.text, buttons)
        

    __mapper_args__ = {
        'polymorphic_identity': 'usertask_submitted'
    }


class UserTaskRejected(Notification):

    def __init__(self, usertask: UserTask):
        db.session.add(self)  # Add the UserTaskRejected object to the session
        db.session.commit()
        super(UserTaskRejected, self).__init__()
        self.usertask = usertask
        self.user = usertask.user
        self.text = f'''The task was rejected. 
Task: {self.usertask.task.name}.
Reason: {self.usertask.rejected_reason}
Fix it and send for review again.'''
        buttons = [{'text': 'Task info', 'url': url_for('tasks.usertask', usertask_id=usertask.id)}]
        self.buttons = json.dumps(buttons)

    def send(self):
        if self.user.telegram_id:
            buttons = json.loads(self.buttons)
            print('sending telegram notification')
            return send_notification(self.user.telegram_id, self.text, buttons)
        

    __mapper_args__ = {
        'polymorphic_identity': 'usertask_rejected'
    }



class NewShop(Notification):

    __mapper_args__ = {
        'polymorphic_identity': 'new_shop'
    }

    def __init__(self, shop: Shop):
        db.session.add(self)  # Add the NewShop object to the session
        db.session.commit()
        super(NewShop, self).__init__()
        self.shop = shop
        self.user = shop.admin.user
        self.text = f'New shop created: {self.shop.name}. You have got 50 points for activating your first task.'
        buttons = [{'text': 'Create new task', 'url': url_for('tasks.add_task', shop_id=shop.id)}]
        self.buttons = json.dumps(buttons)

    def send(self):
        if self.user.telegram_id:
            buttons = json.loads(self.buttons)
            print('sending telegram notification')
            return send_notification(self.user.telegram_id, self.text, buttons)

    
