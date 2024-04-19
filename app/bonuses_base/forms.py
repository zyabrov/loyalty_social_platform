from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired

class NewBonusBaseForm(FlaskForm):
    name_input = StringField('Name')
    type_select = SelectField('Type', choices=[])
    submit = SubmitField('Submit')