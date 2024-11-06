from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, FieldList, FormField, SelectMultipleField, DateTimeField, IntegerField, RadioField, widgets
from wtforms.validators import InputRequired, DataRequired, NumberRange, URL
from flask import url_for, current_app
from app.tasks.models import Task, BaseTask
from app.users.models import User
import os
import json
from app.shops.models import Shop



class GetPostForm(FlaskForm):
    selected = BooleanField('Select', render_kw={
        "class": "form-control",
        # "hx-post": f"/tasks/add_task/post_selected/{id}",
        # "hx-trigger": "change",
    })
    shortcode = HiddenField('shortcode')
    id = HiddenField('id')

class AddTaskForm(FlaskForm):
    points_input = IntegerField('Input Reward (in points)', validators=[InputRequired(), NumberRange(min=1)], render_kw={
        "class": "form-control",        
    })
    rewards_input = IntegerField('Input total quantity of Rewards for this task', validators=[InputRequired(), NumberRange(min=1)], render_kw={
        "class": "form-control",
    })
    description = TextAreaField('Write a tutorial for user')
    checking_type = SelectField('Type of checking', choices=[('Auto check', 'Auto check'), ('Manual check', 'Manual check'), ('AI check', 'AI check')], validators=[], 
                                render_kw={'class': 'form-control',
                                           'hx-post': '/tasks/checking_type_changed',
                                           'hx-target': '#ai_conditions',
                                           'hx-trigger': 'change',
                                }
    )
    repeat_delay = IntegerField('Delay between repeats (hours)', validators=[])
    max_repeats = IntegerField('Max repeats for one user', validators=[])
    ai_conditions = TextAreaField('Conditions for AI to check', validators=[])
    admin_id = HiddenField('admin_id')
    shop_id = HiddenField('shop_id')
    posts = FieldList(FormField(GetPostForm), label="Select posts", 
                      render_kw={'class': 'row'})
    onetime = BooleanField('One reward per user', default=True, render_kw={'checked': True})
    only_followers = BooleanField('Check for following', default=True, render_kw={'checked': True})
    five_words = BooleanField('Minimum 5 words', default=True, render_kw={'checked': True})
    user_category = SelectField('Select User Category', choices=[], validate_choice=False, validators=[])
    
    task_selected = HiddenField('task_selected')
    task_selected_name = HiddenField('task selected name')
    posts_selected = HiddenField('posts selected')
    
    submit = SubmitField('', render_kw={'class': 'btn btn-primary'})

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)

        self.user_category.choices = [(category['name'], category['name']) for category in User.get_categories()]
        if kwargs.get('admin_id'):
            self.admin_id.data = kwargs.get('admin_id')
        if kwargs.get('shop_id'):
            self.shop_id.data = kwargs.get('shop_id')
        if kwargs.get('stage'):
            self.stage.data = kwargs.get('stage')
        if kwargs.get('task_selected'):
            self.task_selected.data = kwargs.get('task_selected')

        self.submit.label.text = 'Publish task'

    def update_user_category_reward(self):
        if self.user_category.data:
            minimal_reward = Task.get_minimal_reward(filter={'category': self.user_category.data, 'checking_type': self.checking_type.data})
            several_reward = Task.get_several_reward(filter={'category': self.user_category.data, 'checking_type': self.checking_type.data})
            max_reward = Task.get_max_reward(filter={'category': self.user_category.data, 'checking_type': self.checking_type.data})
            self.points_input.render_kw['placeholder'] = f'Minimal reward:{minimal_reward} - Several reward: {several_reward} - Max reward: {max_reward}'
            self.points_input.validators = [NumberRange(min=minimal_reward)]


    def update(self, admin_id, shop_id, task_selected, task_selected_name):
        self.admin_id.data = admin_id
        self.shop_id.data = shop_id
        shop = Shop.query.get(self.shop_id.data)
        self.task_selected.data = task_selected
        self.task_selected_name.data = task_selected_name
        if 'Auto' in task_selected_name:
            self.checking_type.data = 'Auto check'
        elif 'Manual' in task_selected_name:
            self.checking_type.data = 'Manual check'
        elif 'AI' in task_selected_name:
            self.checking_type.data = 'AI check'

        if self.task_selected.data == '1':
            from app.instagram.models import InstagramPage
            page = InstagramPage.query.get(shop.instagram_page_id)
            if page:
                if page.posts and len(page.posts) > 0:              
                    for instagram_post in page.posts[:10]:
                        self.posts.append_entry({'shortcode': instagram_post.shortcode, 'id': instagram_post.id})
            if 'Auto' in self.task_selected_name.data:
                self.points_input.validators.append(NumberRange(min=2))
                self.points_input.render_kw['placeholder'] = 'Minimum 2 points'
            else:
                self.points_input.validators.append(NumberRange(min=10))
                self.points_input.render_kw['placeholder'] = 'Minimum 10 points'

    def update_posts(self, posts):
        for post in posts:
            self.posts.append_entry({'shortcode': post.shortcode, 'id': post.id})


class RejectTaskForm(FlaskForm):
    reason = TextAreaField('Reason', validators=[DataRequired()])
    submit = SubmitField('Reject', render_kw={'class': 'btn btn-danger'})
    usertask_id = HiddenField('usertask_id')
        

        

        