from app.extensions import db


company_user = db.Table(
    'company_user',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)


company_location = db.Table(
    'company_location',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),    
)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    logo = db.Column(db.Text)
    main_img = db.Column(db.Text)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    website = db.Column(db.String(120))
    instagram_id = db.Column(db.String(64))
    instagram_username = db.Column(db.String(64))
    facebook_id = db.Column(db.String(64))
    facebook_username = db.Column(db.String(64))
    telegram_bot_id = db.Column(db.String(64))
    telegram_bot_username = db.Column(db.String(64))
    telegram_group_id = db.Column(db.String(64))
    telegram_supergroup_id = db.Column(db.String(64))

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    bonuses = db.relationship('Bonus', backref='company', lazy='dynamic')
    channels = db.relationship('Channel', backref='company', lazy='dynamic')
    rewards = db.relationship('Reward', backref='company', lazy='dynamic')
    certificates = db.relationship('Certificate', backref='company', lazy='dynamic')
    bonusactions = db.relationship('BonusAction', backref='company', lazy='dynamic')
    
    locations = db.relationship('Location', secondary='company_location', backref='companies')
    users = db.relationship('User', secondary='company_user', backref='companies')

    def __repr__(self):
        return '<Company {}>'.format(self.name)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def get(company_id):
        return Company.query.get(company_id)
    

    class Location(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), unique=True, nullable=False)
        description = db.Column(db.Text, nullable=True)
        country = db.Column(db.String(80), nullable=True)
        city = db.Column(db.String(80), nullable=True)
        region = db.Column(db.String(80), nullable=True)
        latitude = db.Column(db.Float, nullable=True)
        longitude = db.Column(db.Float, nullable=True)

