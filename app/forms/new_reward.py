from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired
from app.models import Reward

class NewRewardForm(FlaskForm):
    points_costs = IntegerField('Points Costs', validators=[InputRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

    company_id = HiddenField('company_id')

    def __init__(self, *args, **kwargs):
        super(NewRewardForm, self).__init__(*args, **kwargs)
        self.points_costs.default = 0