from wtforms import StringField, SubmitField, HiddenField, FormField, f
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from app.admins.models import Admin


class AdminSignupForm(FlaskForm):
    user_data = FormField(
        
    )