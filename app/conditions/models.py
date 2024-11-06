from app.extensions import db


class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)


    @classmethod
    def add(cls, name, description=None):
        condition = cls(name=name, description=description)
        db.session.add(condition)
        db.session.commit()
        return condition
    

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def check(self, task, user, usertask=None):
        response = False
        if self.name == 'Only followers':
            response = user.check_following(task.shop_id)
        if self.name == 'Onetime':
            for usertask in user.usertasks:
                if usertask.task.id == task.id and usertask.status != 'Submitted':
                    response = True
        if self.name == 'Minimun 5 words':
            if usertask.comment.text.count(' ') >= 4:
                response = True
        
        if response == False:
            return {'name': self.name, 'response': response}            
        return response
