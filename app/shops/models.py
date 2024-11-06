import os
from app.extensions import db
from app.tags.models import Tag
from flask import current_app


shops_tags = db.Table(
    'shops_tags',
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

shops_addresses = db.Table(
    'shops_addresses',
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'), primary_key=True),
    db.Column('address_id', db.Integer, db.ForeignKey('address.id'), primary_key=True)
)

shop_categories = db.Table(
    'shop_categories',
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    short_description = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    status = db.Column(db.String(80))
    logo_url = db.Column(db.String(80))
    website_url = db.Column(db.String(80))
    instagram_url = db.Column(db.String(80))
    instagram_page_id = db.Column(db.Integer, db.ForeignKey('instagram_page.id'))
    instagram_username = db.Column(db.String(80))
    telegram_group_id = db.Column(db.Integer)
    telegram_bot_id = db.Column(db.String(80))
    youtube_url = db.Column(db.String(80))
    youtube_id = db.Column(db.String(80))
    phone = db.Column(db.Integer, index=True, unique=True)
    country = db.Column(db.String(80))
    region = db.Column(db.String(80))
    city = db.Column(db.String(80))
    address = db.Column(db.String(80))
    instagram_submitted = db.Column(db.Boolean)
    instagram_token = db.Column(db.String(80))
    
    tags = db.relationship('Tag', secondary='shops_tags', backref='shops')
    categories = db.relationship('Category', secondary='shop_categories', backref='shops')
    admin = db.relationship('Admin', backref='shops')
    instagram_page = db.relationship('InstagramPage', backref='shop', uselist=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo_url = os.path.join(current_app.config['SHOPS_UPLOAD_DIR'], self.instagram_username, 'logo.jpg')
    
    def __repr__(self):
        return '<Shop {}>'.format(self.name)
    

    @classmethod
    def add(cls, name, admin_id, instagram_username, phone, logo_url, description=None, website_url=None, country=None, region=None, city=None, address=None, categories=None, telegram_group_id=None, telegram_bot_id=None, youtube_url=None, tags=None):
        print("Values being passed to Shop model's __init__ method:")
        print("name:", name)
        print("description:", description)
        print("admin_id:", admin_id)
        print("website_url:", website_url)
        print("phone:", phone)
        print("country:", country)
        print("region:", region)
        print("city:", city)
        print("address:", address)
        print("categories:", categories)
        shop = cls(name=name, description=description, logo_url=logo_url, admin_id=admin_id, status='new', website_url=website_url, telegram_group_id=telegram_group_id, telegram_bot_id=telegram_bot_id, youtube_url=youtube_url, phone=phone, country=country, region=region, city=city, address=address, instagram_username=instagram_username)
        db.session.add(shop)
        db.session.commit()
        if categories:
            for category in categories:
                from app.shops.models import Category
                shop.categories.append(Category.query.get(category))

        return shop
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    

    def get_and_update_posts(self):
        from app.instagram.models import Instagram, InstagramPost
        instagram = Instagram()
        print('instagram: ', instagram)
        instagram_posts = instagram.get_posts(self.instagram_username)
        print('instagram_posts: ', instagram_posts)
        self.update_posts(instagram_posts, instagram)            
        posts = InstagramPost.query.filter_by(shop_id=self.id).all()
        return posts



    def update_posts(self, instagram_posts, instagram):
        from app.instagram.models import InstagramPost, Instagram
        print('shop instagram posts: ', InstagramPost.query.filter_by(shop_id=self.id).all())
        updated_posts = []
        for instagram_post in instagram_posts:
            print('instagram post shortcode: ', instagram_post.shortcode)
            if instagram_post.shortcode not in [post.shortcode for post in InstagramPost.query.filter_by(shop_id=self.id).all()]:
                post = InstagramPost.add(shortcode=instagram_post.shortcode, caption=instagram_post.caption, shop_id=self.id)
                print('new post: ', post)
                instagram.save_image(image_url=instagram_post.url, image_name=post.shortcode, username=self.instagram_username)
                print('post image saved')
        return updated_posts
    

    def delete_posts(self):
        from app.instagram.models import InstagramPost
        for post in self.instagram_posts:
            InstagramPost.query.filter_by(shortcode=post.shortcode).delete()
        db.session.commit()

    def get_logo(self):
        return os.path.join('/static', 'uploads', 'shops', self.instagram_username, 'logo.jpg')

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80), unique=False, nullable=False)

    
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(80), unique=False, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref='regions', uselist=False)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=False, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    region = db.relationship('Region', backref='cities', uselist=False)
    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(80), unique=False, nullable=False)
    longitude = db.Column(db.String(80), unique=False, nullable=False)
    country = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    region = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    
company_categories = [{
    'category': 'Food',
    'names': ['Groceries', 'Restaurants', 'Bars', 'Cafes', 'Fast food', 'Pubs', 'Cafeteria', 'Catering']
}, {
    'category': 'Travel',
    'names': ['Travel agency', 'Hotels', 'Cruises']
}, {
    'category': 'Entertainment',
    'names': ['Cinema', 'Theater', 'Gaming']
}, {
    'category': 'Shopping',
    'names': ['Flowers', 'Gifts', 'Tickets']
}, {
    'category': 'Health',
    'names': ['Pharmacy', 'Doctor']
}, {
    'category': 'Pets',
    'names': ['Pet store']
}, {
    'category': 'Services',
    'names': ['Cleaning', 'Carpentry', 'Hairing', 'Judge', 'Teaching']
}, {
    'category': 'Education',
    'names': ['School', 'University']
}, {
    'category': 'IT',
    'names': ['Web development', 'App development']
}]

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    childs = db.relationship('Category', backref='parent', remote_side=[id])

    @classmethod
    def add_base_categories(cls):
        for i in range(len(company_categories)):
            category = company_categories[i]
            new_category = cls(name=category['category'], parent_id=None)
            print('new_category: ', new_category)
            db.session.add(new_category)
            db.session.commit()
            for name in category['names']:
                new_subcategory = cls(name=name, parent_id=new_category.id)
                db.session.add(new_subcategory)
                print('new_subcategory: ', new_subcategory)
                db.session.commit()
