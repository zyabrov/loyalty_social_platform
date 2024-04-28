from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Email, Length

class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email('Please enter a valid email address')])
    password = StringField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Register')