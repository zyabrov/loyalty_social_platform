# from instaloader import Instaloader, Profile, Post
# from instaloader.exceptions import ConnectionException, QueryReturnedBadRequestException
import time
from config import Config
from datetime import datetime
import os
from flask import current_app
from app import db
import requests
import instaloader


class Instagram():
    def __init__(self, api_token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_token = api_token
        self.url = 'https://graph.facebook.com/v21.0/'
    
    def get_instagram_page_id(self):
        r = requests.get(self.url + 'me/accounts', params={'fields': 'connected_instagram_account', 'access_token': self.api_token})
        print('response: ', r, r.text, r.status_code)
        if r.status_code == 200:
            data = r.json()
            if data['data']:
                id = data['data'][0]['connected_instagram_account']['id']
                return id
    
    def get_instagram_page_data(self, page_id:int):
        url = f'{self.url}{page_id}'
        r = requests.get(url, params={'fields': 'name,profile_picture_url,website,username,biography,media_count,media,tags,recently_searched_hashtags,followers_count,follows_count', 'access_token': self.api_token})
        print(r.text)
        if r.status_code == 200:
            data = r.json()
            return data
        
    def get_instagram_page_posts(self, page_id):
        page_data = self.get_instagram_page_data(page_id)
        posts = page_data['media']['data']
        return posts

    def get_post_data(self, post_id):
        r = requests.get(self.url + str(post_id), params={'fields': 'comments_count,caption,like_count,media_type,owner,media_url,permalink,shortcode,thumbnail_url,timestamp,comments{from,text,timestamp,user,username,replies}', 'access_token': self.api_token})
        print(r.text)
        if r.status_code == 200:
            data = r.json()
            return data
        
    def get_comments(self, post_id):
        post_data = self.get_post_data(post_id)
        comments = post_data['comments']['data']
        return comments



class InstagramPage(db.Model):
    __tablename__ = 'instagram_page'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    profile_pic = db.Column(db.String(80))
    website = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True, nullable=False)
    biography = db.Column(db.String(80))
    media_count = db.Column(db.Integer)
    saved_profile_pic_url = db.Column(db.String(80))
    tags = db.Column(db.String(80))
    searched_hashtags = db.Column(db.JSON)
    followers_count = db.Column(db.Integer)
    follows_count = db.Column(db.Integer)
    follows = db.Column(db.JSON)
    followers = db.Column(db.JSON)
    last_updated = db.Column(db.DateTime)
    


    @classmethod
    def add(cls, id, name, username, profile_pic, biography, media_count=None, followers_count=None, follows_count=None, shop_id=None, user_id=None, website=None, posts=None, stories=None, tags=None, searched_hashtags=None, follows=None, followers=None):
        saved_profile_pic_url = None
        if shop_id:
            from app.shops.models import Shop
            shop = Shop.query.get(shop_id)
            if profile_pic:
                dir_path = os.path.join(current_app.root_path, 'static', 'uploads', 'shops', username)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                saved_profile_pic_url = cls.save_profile_pic(profile_pic, dir_path)
        elif user_id:
            from app.users.models import User
            user = User.query.get(user_id)
            if profile_pic:
                dir_path = os.path.join(current_app.root_path, 'static', 'uploads', 'users', username)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                saved_profile_pic_url = cls.save_profile_pic(profile_pic, dir_path)
        if searched_hashtags:
            print('searched_hashtags: ', searched_hashtags)
            searched_hashtags = [hashtag.text for hashtag in searched_hashtags]
        if followers:
            print('followers: ', followers)
            followers = [follower.username for follower in followers]
            followers_count = len(followers)

        if follows:
            print('follows: ', follows)
            follows = [follow.username for follow in follows]
            follows_count = len(follows)

        page = InstagramPage(
            id = id,
            name = name,
            username = username,
            profile_pic = profile_pic,
            biography = biography,
            media_count = media_count,
            website = website,
            saved_profile_pic_url = saved_profile_pic_url,
            tags = tags,
            searched_hashtags = searched_hashtags,
            followers_count = followers_count,
            follows_count = follows_count,
            follows = follows,
            followers = followers,
            last_updated = datetime.now()
        )
        db.session.add(page)
        if shop_id:shop.instagram_page = page
        elif user_id:user.instagram_page = page
        db.session.commit()
        return cls
    
    @classmethod
    def save_profile_pic(self, image_url, dir_path):
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            with open(os.path.join(dir_path, 'logo.jpg'), 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            return os.path.join(dir_path, 'logo.jpg')
        else:
            return None


class InstagramPost(db.Model):
    __tablename__ = 'instagram_post'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('instagram_page.id'))    
    shortcode = db.Column(db.String(80), unique=True, nullable=False)
    caption = db.Column(db.String(80), unique=False, nullable=True)
    image_url = db.Column(db.String(80))
    url = db.Column(db.String(80))
    saved_media_url = db.Column(db.String(80))
    media_type = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime)

    page = db.relationship('InstagramPage', backref='posts')


    def __repr__(self):
        return f'<InstagramPost {self.shortcode}>'


    @classmethod
    def add(cls, id, shortcode, caption, media_type, image_url, url, page_id, timestamp):
        page = InstagramPage.query.get(page_id)
        _timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
        post = InstagramPost(
            id = id,
            shortcode=shortcode,
            caption=caption,
            media_type=media_type,
            image_url=image_url,
            url=url,
            page_id=page_id,
            timestamp=_timestamp,
            saved_media_url=os.path.join('/static', 'uploads', 'shops', page.username, 'posts', shortcode + '.jpg')
        )
        db.session.add(post)
        db.session.commit()
        return cls
    
class InstagramProfile(db.Model):
    __tablename__ = 'instagram_profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    url = db.Column(db.String(80), unique=True, nullable=False)
    profile_pic = db.Column(db.String(80))
    biography = db.Column(db.String(80))
    media_count = db.Column(db.Integer)
    saved_profile_pic_url = db.Column(db.String(80))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))
    post_id = db.Column(db.Integer, db.ForeignKey('instagram_post.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('instagram_page.id'))
    timestamp = db.Column(db.DateTime)

    post = db.relationship('InstagramPost', backref='comments')
    owner = db.relationship('InstagramPage', backref='comments')

    @classmethod
    def add(cls, id, post_id, owner_id, text, timestamp, usertask=None):
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
        comment = Comment(
            id=id,
            post_id=post_id,
            owner_id=owner_id,
            text=text,
            timestamp=timestamp,
        )
        db.session.add(comment)
        print('comment added: ', comment)
        if usertask:
            usertask.add_comment(comment)
            print('comment added to usertask: ', usertask.comment)
        db.session.commit()
        return cls

    

class Instaloader():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.L = instaloader.Instaloader(download_comments=True)
        self.profile = None
        try:
            self.L.load_session_from_file(username='loyaltybots', filename='instaloader_session_loyaltybots')
        except FileNotFoundError:
            if not self.L.context.is_logged_in:
                self.login()


    def download_profile(self, username):
        profile = self.L.download_profile(username, profile_pic=True)
        print('profile downloaded: ', profile)
        return profile

    def login(self):
        self.L.login('loyaltybots', 'E2yZ_5#Q@<84*Tg')
        # self.L.login('mziabrov', 'ZMixan29031990**')
        print('login successful')
        self.L.save_session_to_file(filename='instaloader_session_loyaltybots')

    def get_profile(self, username):
        self.profile = instaloader.Profile.from_username(self.L.context, username)
        if self.profile:
            print('profile loaded: ', self.profile.username)
        return self.profile
    

    def get_followers(self, username):
        if self.profile is None:
            self.get_profile(username)
        print('followers loaded')
        return self.profile.get_followers()


    # def load_profile(self):
        # upload_folder = os.path.join(Config.UPLOAD_FOLDER, 'instagram_sessions')
        # if not os.path.exists(upload_folder):
        #     os.makedirs(upload_folder)
        # session_path = os.path.join(upload_folder,'instaloader_session_' + self.username)
        # try:
        #     with open(session_path, 'rb') as session_file:
        #         self.L.context.load_session_from_file(sessionfile=session_file, username=self.username)
        #         print('session loaded')
        # except Exception as e:
        #     print(f"Failed to load session: {e}")
        # try:
    #         with self.L.context.login('mziabrov', 'ZMixan29031990**'):

    #             print('login successful')
    #             with open(session_path, 'wb') as session_file:
    #                 self.L.context.save_session_to_file(sessionfile=session_file)
    #                 print('session created')
    #     except self.L.exceptions.InstaloaderException as e:
    # print(f"Failed to login: {e}")

#     def get_posts(self, username):
#         if self.profile is None:
#             self.get_profile(username)
        
#             posts = Profile.from_username(self.L.context, username).get_posts()
#         else:
#             posts = self.profile.get_posts()
#         return posts
    

    
#     def get_post_comments(self, shortcode):
#         comments = None
#         max_retries = 5
#         retry_delay = 60
#         for i in range(max_retries):
#             try:
#                 self.L.update_comments(filename='instaloader_comments_loyaltybots', post=Post.from_shortcode(self.L.context, str(shortcode)))
#                 break
#             except ConnectionException or QueryReturnedBadRequestException as e:
#                 print(f"Error: {e}")
#                 time.sleep(retry_delay)
#                 retry_delay *= 2  # double the delay for each retry
#         if comments:
#             print('comments loaded: ')
#             for comment in comments:
#                 print(comment.text)
#         return comments
    

    def save_profile_pic(self, username, image_url):
        target_dir = os.path.join(current_app.config['USERS_UPLOAD_DIR'], username)
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        self.L.download_pic(url=image_url, filename=target_dir + '/' + 'logo', mtime=datetime.now())
        print('profile pic saved: ', target_dir + '/' + 'logo.jpg')
        return target_dir + '/' + 'logo.jpg'
    
    def check_following(self, username, username_to_check):
        followers = self.get_followers(username)
        for follower in followers:
            print(follower.username)
            if follower.username == username_to_check:
                return True
        return False
