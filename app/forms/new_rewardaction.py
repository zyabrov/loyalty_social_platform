from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired
from app.models import Reward, User


class NewRewardActionForm(FlaskForm):
    user = SelectField('user', choices=[])
    reward = SelectField('Reward', choices=[])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(NewRewardActionForm, self).__init__(*args, **kwargs)
        print(Reward.query.all())
        self.reward.choices = [(reward.id, reward.name) for reward in Reward.query.all()]
        self.user.choices = [(user.id, user.username) for user in User.query.all()]