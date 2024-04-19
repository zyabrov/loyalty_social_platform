from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired
from app.bonuses.models import Bonus 
from app.users.models import User


class NewBonusActionForm(FlaskForm):
    user = SelectField('user', choices=[])
    bonus = SelectField('Bonus', choices=[])
    company = HiddenField('company')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(NewBonusActionForm, self).__init__(*args, **kwargs)
        print(Bonus.query.all())
        self.bonus.choices = [(bonus.id, bonus.name) for bonus in Bonus.query.all()]
        self.user.choices = [(user.id, user.username) for user in User.query.all()]