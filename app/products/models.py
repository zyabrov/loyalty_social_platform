from extensions import db


product_user = db.Table(
    'product_user',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


product_tag = db.Table(
    'product_tag',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    points_cost = db.Column(db.Integer)
    short_description = db.Column(db.Text)
    description = db.Column(db.Text)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    shop = db.relationship('Shop', backref='product', uselist=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    users = db.relationship('User', secondary='product_user', backref='product')
    type = db.Column(db.String(80))
    standart_cost = db.Column(db.Integer)
    currency = db.Column(db.String(80))
    available_quantity = db.Column(db.Integer)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(80))
    tags = db.relationship('Tag', secondary='product_tag', backref='product')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    

    def __repr__(self):
        return '<Product {}>'.format(self.name)
    
    @classmethod
    def add(cls, name, points_cost, short_description, description, shop_id, type, standart_cost, currency, available_quantity, end_date, category_id, subcategory_id):
        product = Product(
            name = name,
            points_cost = points_cost,
            short_description = short_description,
            description = description,
            shop_id = shop_id,
            type = type,
            standart_cost = standart_cost,
            currency = currency,
            available_quantity = available_quantity,
            end_date = end_date,
            status = 'active',
            category_id = category_id,
            subcategory_id = subcategory_id
        )
        db.session.add(product)
        db.session.commit()
        return product


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)
    

class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<SubCategory {}>'.format(self.name)