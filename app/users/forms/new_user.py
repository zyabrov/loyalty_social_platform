from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Email

class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email('Please enter a valid email address')])
    phone = StringField('Phone', validators=[InputRequired()])
    submit = SubmitField('Submit')