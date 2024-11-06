from wtforms import StringField, SubmitField, HiddenField, TextAreaField, FileField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm


class NewProductForm(FlaskForm):
    shop_id = HiddenField()
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    short_description = StringField('Short description', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    logo = FileField('Logo')
    main_image = FileField('Main image')
    images = FileField('Images')
    type = SelectField('Type', choices=[('product', 'Product'), ('service', 'Service')])
    points_cost = IntegerField('Points cost')
    standart_cost = IntegerField('Standart cost')
    currency = SelectField('Currency', choices=[('hrn', 'HRN'), ('usd', 'USD'), ('eur', 'EUR')])
    available_quantity = IntegerField('Available quantity')
    end_date = DateTimeField('End date')
    category = SelectField('Category', choices=[])
    subcategory = SelectField('Subcategory', choices=[])
    submit = SubmitField('Create')


    def __init__(self, *args, **kwargs):
        super(NewProductForm, self).__init__(*args, **kwargs)
        from app.products.models import Category, SubCategory
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
        if self.category.data:
            self.subcategory.choices = [(subcategory.id, subcategory.name) for subcategory in SubCategory.query.filter_by(category_id=self.category.data)]