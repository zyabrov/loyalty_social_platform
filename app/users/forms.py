from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField, TelField, PasswordField, EmailField
from wtforms.validators import InputRequired, DataRequired, Email, Regexp, Length, NumberRange
from datetime import datetime


class SignUpForm(FlaskForm):
    user_type = HiddenField()
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email('Please enter a valid email address')])
    phone = TelField('Phone', validators=[InputRequired(), Regexp(regex='^\\+380\\d{9}$', message='Please enter a valid phone number')], render_kw={"placeholder": "+380XXXXXXXXX"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, message="Password must contain at least 6 characters")])
    

    country = StringField('Your country')
    city = StringField('Your city')
    birthday = DateTimeField('Your birthday')
    
    age = HiddenField()
    referrer_id = HiddenField()
    
    submit = SubmitField('Sign up')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.birthday.data:
            self.age.data = (datetime.now() - self.birthday.data).days // 365


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email('Please enter a valid email address')])
    phone = TelField('Phone', validators=[Regexp(regex='^\\+380\\d{9}$', message='Please enter a valid phone number')], render_kw={"placeholder": "+380XXXXXXXXX"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, message="Password must contain at least 6 characters")])
    submit = SubmitField('Login')


class AddPointsForm(FlaskForm):
    user_id = SelectField('Select user', validators=[DataRequired()])
    points_input = IntegerField('Input the amount of points', validators=[DataRequired(), NumberRange(min=1)])
    reason = StringField('Input the reason', validators=[DataRequired()])
    submit = SubmitField('Add points', render_kw={'class': 'btn btn-primary'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.users.models import User
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]
        print(self.user_id.choices)


class AddInstagramForm(FlaskForm):
    user_id = HiddenField('user_id')
    instagram_username = StringField('Input your instagram username', validators=[DataRequired()])
    # is_follower = BooleanField('I am a follower', default=False, render_kw={'checked': False})
    submit = SubmitField('Add profile', render_kw={'class': 'btn btn-primary', 'hx-target': '#pop-up', 'hx-swap': 'innerHTML'})