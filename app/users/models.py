from app.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.shops.models import Shop
from app.instagram.models import Instaloader, InstagramPage
import os
from flask import current_app

users_tags = db.Table(
    'users_tags',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
)

users_shops = db.Table(
    'users_shops',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'), primary_key=True),
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.Integer, index=True, unique=True)
    country = db.Column(db.String(80))
    city = db.Column(db.String(80))
    birthday = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer)
    registered = db.Column(db.DateTime, default=datetime.now)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=0)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5), default='en')
    user_type = db.Column(db.String(80))
    blocked_points = db.Column(db.Integer, default=0)
    instagram_submitted = db.Column(db.Boolean, default=False)
    saved_profile_pic_url = db.Column(db.String(80))
    instagram_page_id = db.Column(db.Integer, db.ForeignKey('instagram_page.id'))
    telegram_id = db.Column(db.Integer, unique=True)
    telegram_username = db.Column(db.String(80))
    category = db.Column(db.String(80))
    currency = db.Column(db.String(80), default='USD')

    instagram_page = db.relationship('InstagramPage', backref='user', uselist=False)
    shops = db.relationship('Shop', secondary=users_shops, backref='users')
    tags = db.relationship('Tag', secondary=users_tags, backref='users')
    referrer = db.relationship('User', remote_side=[id])


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.referrer_id:
            self.referrer = User.query.get(self.referrer_id)
        if self.instagram_page:
            if self.instagram_page.profile_pic_url:
                self.saved_profile_pic_url = os.path.join(current_app.config['USERS_UPLOAD_DIR'], self.instagram_username, 'logo.jpg')
            if self.instagram_page.followers_count:
                self.set_category(self.instagram_page.followers_count)
            
    
    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_category(self, followers_count):
        categories = self.get_categories()
        for category in categories:
            if followers_count <= category['followers_count']:
                self.category = category['name']
                break

        if not self.category:
            self.category = categories[-1]['name']

        self.update(category=self.category)


    @classmethod
    def get_categories(cls):
        return [{'name':'Newbie', 'followers_count':100}, {'name':'Amateur', 'followers_count':1000}, {'name':'Professional', 'followers_count':10000}, {'name':'Star', 'followers_count':100000}, {'name':'All'}]
    
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_by_name(name):
        return User.query.filter_by(name=name).first()

    @classmethod
    def add(cls, name, email, phone, password, user_type, referrer_id=None):

        user = User(
            name=name,
            email=email,
            phone=phone,
            registered=datetime.now(),
            referrer_id=referrer_id,
            user_type=user_type, 
        )
        db.session.add(user)
        user.set_password(password)
        db.session.commit()
        return user
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()


    def add_points(self, points, reason, from_user_id=None, task_id=None):
        name = ''
        if points < 0:
            name = 'Removed points'
        else:
            name = 'Added points'
        from app.actions.models import PointsAction
        PointsAction.add(points, self.id, name, reason, from_user_id, task_id)
        self.points += points
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



    def check_following(self, shop_id):
        from app.shops.models import Shop
        from app.instagram.models import Instagram
        shop = Shop.query.get(shop_id)
        print('shop instagram username: ', shop.instagram_page.username)
        instagram = Instaloader()
        shop_followers = instagram.get_followers(username=shop.instagram_page.username)
        print('shop followers: ', shop_followers)
        for follower in shop_followers:
            print(follower)
            if self.instagram_page.username == follower.username:
                print('folower was founded')
                return True
        return False
    
    


    def delete(self):
        from app.tasks.models import UserTask
        UserTask.query.filter_by(user_id=self.id).delete()
        from app.notifications.models import Notification
        Notification.query.filter_by(user_id=self.id).delete()
        from app.shops.models import Shop
        shop_users = Shop.query.filter(Shop.users.any(id=self.id)).all()
        if self in shop_users:
            shop_users.remove(self)
        db.session.delete(self)
        db.session.commit()

    def save_instagram_profile(self, username) -> InstagramPage:
        self.instagram_username = username
        instagram = Instaloader()
        profile = instagram.get_profile(username)
        if profile:
            print('profile data: ', profile)
            instagram_page = InstagramPage.query.filter_by(username=username).first()
            if not instagram_page:
                instagram_page = InstagramPage.add(
                    id=profile.userid,
                    user_id=self.id,
                    name=profile.full_name,
                    username=username,
                    profile_pic=profile.profile_pic_url,
                    biography=profile.biography,
                    follows = profile.get_followees(),
                    followers = profile.get_followers(),
                    searched_hashtags = profile.get_followed_hashtags(),
                )
        return instagram_page
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class SuperAdmin(User):
    def __init__(self, **kwargs):
        super(SuperAdmin, self).__init__(**kwargs)
        self.user_type = 'superadmin'
