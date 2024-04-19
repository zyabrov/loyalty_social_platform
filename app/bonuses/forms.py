from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, DataRequired
from app.bonuses_base.models import BonusBase 
from app.rewards.models import Reward


class NewBonusForm(FlaskForm):
    bonus_base_id = SelectField('Base Bonus', coerce=int, choices=[], validators=[InputRequired()], render_kw= {
            "class": "form-control",
            "type": "select",
            "placeholder": "Select Bonus",
            "hx_trigger": "change",
            "hx-post": "/bonuses/basebonus_selected",
            "id": "base_bonus_select",
            "hx-target": "#points_value",
            "hx-swap": "innerHTML"
        })
    points_value = IntegerField('Points Value', validators=[InputRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(NewBonusForm, self).__init__(*args, **kwargs)
        base_bonuses = BonusBase.query.all()
        self.bonus_base_id.choices = [(b.id, b.name) for b in base_bonuses]
        if base_bonuses:
            self.points_value.data = base_bonuses[0].base_amount

    def update_points_value(self, base_bonus):
        self.points_value.data = base_bonus.base_amount
        

        