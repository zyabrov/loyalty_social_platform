from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Email, Length

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = StringField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Submit')