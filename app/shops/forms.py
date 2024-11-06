from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, FileField, TelField, BooleanField, SearchField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, URL, Regexp, InputRequired
from flask_wtf import FlaskForm
from app.extensions import geo_plug
from flask import jsonify
from app.shops.models import Category



class NewShopForm(FlaskForm):
    admin_id = HiddenField()
    name = StringField('Your Company name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=500)])
    logo = FileField('Logo')
    category = SelectField('Category', validators=[InputRequired()], choices=[], render_kw={
        "class": "form-control",
        "type": "select",
        "hx-trigger": "change",
        "hx-post": "/shops/update_subcategories",
        "hx-target": "#subcategories",
        "hx-swap": "outerHTML"
    })
    subcategories = SelectField('Subcategories', validate_choice=False, validators=[DataRequired()], choices=[], render_kw={
        "class": "form-control", "type": "select"
    })
    phone = TelField('Phone', validators=[Regexp(regex='^\\+380\\d{9}$', message='Please enter a valid phone number')], render_kw={"placeholder": "+380XXXXXXXXX", "class": "form-control"})
    website_url = StringField('Website URL', validators=[URL(), Length(max=100)], render_kw={"class": "form-control"})
    instagram_username = HiddenField()
    # facebook_url = StringField('Facebook URL', validators=[URL(), Length(max=100)], render_kw={"class": "form-control"})  
    # telegram_bot_url = StringField('Telegram Bot URL', validators=[URL(), Length(max=100)], render_kw={"class": "form-control"})
    # telegram_group_url = StringField('Telegram Group URL', validators=[URL(), Length(max=100)], render_kw={"class": "form-control"})
    # youtube_url = StringField('Youtube Channel URL', validators=[URL(), Length(max=100)], render_kw={"class": "form-control"})

    # has_offline = BooleanField('Has offline points', default=False, render_kw={"class": "form-control"})  
    # google_maps_url = StringField('Google Maps URL', validators=[URL(), Length(max=100)], render_kw={"class": "form-control"})
    country = SelectField('Select Country', validate_choice=False, validators=[Length(max=100)], choices=[], render_kw={
        "class": "form-control",
        "type": "select",
        "hx-trigger": "change",
        "hx-post": "/shops/update_regions",
        "hx-target": "#region",
        "hx-swap": "outerHTML"
        })
    region = SelectField('Select Region', validate_choice=False, validators=[Length(max=100)], choices=[], render_kw={
        "class": "form-control",
        "type": "select",
        "hx-trigger": "change",
        "hx-post": "/shops/update_cities",
        "hx-target": "#city",
        "hx-swap": "outerHTML"
    })
    city = SelectField('Select City',validate_choice=False, validators=[Length(max=100)], choices=[], render_kw={
        "class": "form-control",
        "type": "select"
    })
    address = StringField('Address', validators=[Length(max=100)])
    logo_filename = HiddenField()
    logo_url = HiddenField()
    instagram_id = HiddenField()

    # tags = SearchField('Tags', validators=[InputRequired()])
    submit = SubmitField('Create')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.tags.get_data = self.get_tags
        self.category.choices = [('', 'Select category')] + [(category.id, category.name) for category in Category.query.filter_by(parent_id=None).all()]
        all_countries = geo_plug.all_CountryNames()
        self.country.choices = [('', 'Select country')] + [(country, country) for country in all_countries]


    def update_regions(self):
        country = self.country.data
        regions = geo_plug.Country_all_StateNames(country)
        self.region.choices = [('', 'Select region')] + [(region, region) for region in regions]

    def update_cities(self):
        region = self.region.data
        cities = geo_plug.all_State_CityNames(region)
        self.city.choices = [('', 'Select city')] + [(city, city) for city in cities]

    def update_subcategories(self):
        category = self.category.data
        subcategories = Category.query.filter_by(parent_id=int(category)).all()
        self.subcategories.choices = [('', 'Select subcategory')] + [(subcategory.id, subcategory.name) for subcategory in subcategories]


    def get_tags(self):
        from app.tags.models import Tag
        return [(tag.id, tag.name) for tag in Tag.query.filter_by(type='shop').all()]

    #Todo: 
    # - get data from google_maps: website_url, address
    # - authorization with Instagram


class AddInstagramForm(FlaskForm):
    instagram_username = StringField('Input your instagram username', validators=[DataRequired()])
    submit = SubmitField('Check following', render_kw={'class': 'btn btn-primary'})