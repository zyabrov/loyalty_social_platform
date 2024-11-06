from app.shops import bp
from flask import render_template, request, current_app, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from app.shops.forms import NewShopForm
import os
from flask_login import login_required, current_user
from app.admins.models import Admin
from app.shops.models import Shop
from app.extensions import geo_plug
from app.shops.forms import AddInstagramForm
from datetime import datetime
import requests
import json 

@bp.route('/', methods=['GET'])
@login_required
def shops():
    return render_template('shops.html', user=current_user)


@bp.route('/shop/<int:shop_id>', methods=['GET'])
@login_required
def shop(shop_id):
    shop = Shop.query.get(shop_id)
    return render_template('shop.html', shop=shop, user=current_user)


@bp.route('/add_instagram_profile', methods=['GET', 'POST'])
@login_required
def add_instagram_profile():
    from app.shops.forms import AddInstagramForm
    form = AddInstagramForm(formdata=request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            print('form is valid')
            if check_app_following(form.instagram_username.data) == True:
                print('user is following app')
                return redirect(url_for('shops.new_shop', instagram_username=form.instagram_username.data))
            
            else:
                form.errors['instagram_username'] = 'Instagram account not found in followers list'
        else:
            print('form errors: ', form.errors)

    return render_template('add_instagram_profile.html', form=form)

def get_profile_data(instagram_username):
    from app.instagram.models import Instagram
    instagram = Instagram()
    profile = instagram.get_profile(instagram_username)
    print('profile', profile)
    print('id:', profile.userid)
    print('username:', profile.username)
    print('full name:', profile.full_name)
    print('biography:', profile.biography)
    print('external url:', profile.external_url)
    print('profile pic url:', profile.profile_pic_url)
    #save profile pic:
    if profile.profile_pic_url:
        instagram.save_profile_pic(profile.username, profile.profile_pic_url)
    return profile


@bp.route('/new_shop', methods=['GET', 'POST'])
@login_required
def new_shop():
    form = NewShopForm(formdata=request.form)
    admin = Admin.get_by_user_id(current_user.id)
    if request.method == 'GET':
        print('new shop request: ', request.args)
        if 'instagram_username' in request.args:
            form.instagram_username.process_data(request.args.get('instagram_username'))
            profile = get_profile_data(request.args.get('instagram_username'))
            form.name.process_data(profile.full_name)
            form.description.process_data(profile.biography)
            form.website_url.process_data(profile.external_url)
            form.logo_url.process_data(profile.profile_pic_url)
            form.instagram_id.process_data(profile.userid)
        form.admin_id.process_data(admin.id)

    elif request.method == 'POST':
        print('new shop post request: ', request.form)
        shops_folder = current_app.config['SHOPS_UPLOAD_DIR']
        if not os.path.exists(shops_folder):
            os.makedirs(shops_folder)
        
        if form.validate_on_submit():
            print('form is valid')
            categories = [int(form.category.data)] + [int(form.subcategories.data)]
            shop = Shop.add(
                name=form.name.data, 
                description=form.description.data, 
                admin_id=form.admin_id.data, 
                instagram_username=form.instagram_username.data,
                categories=categories,
                phone=form.phone.data,
                website_url=form.website_url.data,
                country=form.country.data,
                region=form.region.data,
                city=form.city.data,
                address=form.address.data,
                # logo_filename=form.logo.data
                )
            # # save logo
            # file = request.files.getlist('logo')[0]
            # file_name = request.files.getlist('logo')[0].filename
            # logo_filename = secure_filename(file_name)
            # print('logo_filename: ', logo_filename)
            # file.save(os.path.join(shops_folder, f'{shop.id}, {logo_filename}'))
            # print('file saved in shops folder')
            # update admin.current_shop
            shop.get_and_update_posts()
            admin.update_current_shop(shop.id)
            admin.add_points(50)
            flash('Shop has been created', 'message')
            return redirect(url_for('dashboard.dashboard'))
        else:
            print('form is not valid')
            print(form.errors)
            return render_template('new_shop_form.html', form=form)
        
    print('form data: ', form.data)
    return render_template('new_shop.html', form=form, admin=admin)


@bp.route('/update_regions', methods=['POST'])
def update_regions():
    form = NewShopForm(formdata=request.form)
    form.update_regions()
    return render_template('region.html', form=form)


@bp.route('/update_subcategories', methods=['POST'])
def update_subcategories():
    form = NewShopForm(formdata=request.form)
    form.update_subcategories()
    return render_template('subcategories.html', form=form)

@bp.route('/update_cities', methods=['POST'])
def update_cities():
    form = NewShopForm(formdata=request.form)
    form.update_cities()
    return render_template('city.html', form=form)


@bp.route('/get_posts', methods=['GET', 'POST'])
def get_posts():
    admin = Admin.get_by_user_id(current_user.id)
    shop = Shop.query.get(admin.current_shop.id)
    shop_username = shop.instagram_username
    print('shop username: ', shop_username)
    shop_posts = shop.get_and_update_posts()
    return shop_posts



@bp.route('/add_task', methods=['GET'])
def add_task():
    from app.tasks.models import BaseTask
    tasks = BaseTask.query.all()
    admin = Admin.get_by_user_id(current_user.id)
    return render_template('select_task.html', tasks=tasks, admin=admin)


@bp.route('/task_selected/<int:basetask_id>', methods=['GET'])
def task_selected(basetask_id):
    if basetask_id == 1:
        return render_template('add_comment_task.html')
    else:
        from app.tasks.routes import add_task
        return add_task(basetask_id)


@bp.route('/delete_posts', methods=['GET'])
def delete_posts():
    admin = Admin.get_by_user_id(current_user.id)
    shop = Shop.query.get(admin.current_shop.id)
    shop.delete_posts()
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/logo/<int:shop_id>', methods=['GET'])
def shop_logo(shop_id):
    shop = Shop.query.get(shop_id)
    logo = shop.get_logo()
    return logo
    

@bp.route('/check_app_following/<string:instagram_username>', methods=['POST'])
def check_app_following(instagram_username):
    from app.instagram.models import Instagram
    superadmin_shop = Shop.query.get(1)
    print('superadmin_shop instagram username: ', superadmin_shop.instagram_username)
    i = Instagram()
    if i.check_following(username=superadmin_shop.instagram_username, username_to_check=instagram_username):
        print('user is following app')
        return True
    else:
        print('user is not following app')
        return False


@bp.route('/instagram_submit', methods=['POST'])
@login_required
def instagram_submit():
    form = AddInstagramForm(formdata=request.form)
    admin = Admin.get_by_user_id(current_user.id)
    print('admin: ', admin)
    shop = admin.current_shop
    if form.validate_on_submit():
        shop.instagram_username = form.instagram_username.data
        if check_app_following(shop.id):
            shop.instagram_submitted = True
            shop.update(instagram_username=shop.instagram_username, instagram_submitted=shop.instagram_submitted)
            flash('Instagram profile has been activated', 'message')
            return redirect (url_for('tasks.tasks'))
        else:
            print('form is not valid')
            form.errors['instagram_username'] = ['Instagram account not found in followers list']
            return render_template('instagram_submit_form.html', form=form)
    else:
        print('form is not valid')
        print(form.errors)
        return render_template('instagram_submit_form.html', form=form)
    
        
@bp.route('/save_instagram_profile', methods=['GET', 'POST'])
@login_required
def save_instagram_profile():
    shop = Admin.get_by_user_id(current_user.id).current_shop
    from app.instagram.models import Instagram, InstagramPost, InstagramProfile, Comment, InstagramPage
    i = Instagram(shop.instagram_token)
    page_id = i.get_instagram_page_id()
    print('page_id: ', page_id)
    page_data = i.get_instagram_page_data(page_id)
    print('page_data: ', page_data)
    page = InstagramPage.query.get(page_id)
    if page:
        print('page already exists')
    else:
        print('page does not exist, creating')
        page = InstagramPage.add(id=page_id, shop_id=shop.id, name=page_data.get('name'), username=page_data.get('username'), profile_pic=page_data.get('profile_picture_url'), biography=page_data.get('biography', None), media_count=page_data['media_count'], website=page_data.get('website', None), posts=page_data['media'].get('data', None), followers_count=page_data.get('followers_count', None), follows_count=page_data.get('follows_count', None), tags=page_data.get('tags', None), searched_hashtags=page_data.get('searched_hashtags', None))
        # page = InstagramPage.add(page_data=page_data)
        print('page: ', page)
    posts = i.get_instagram_page_posts(page_id)
    print('posts: ', posts)
    if posts:
        for post in posts:
            post_data = i.get_post_data(post['id'])
            print('post_data: ', post_data)
            if InstagramPost.query.get(post['id']):
                print('post already exists')
            else:
                print('post does not exist, creating')
                post = InstagramPost.add(id=post_data['id'], shortcode=post_data['shortcode'], caption=post_data.get('caption', None), media_type=post_data['media_type'], image_url=post_data['media_url'], url=post_data['permalink'], page_id=page.id, timestamp=post_data['timestamp'])
                print('post: ', post)
    return {'status': '200', 'message': 'Instagram profile has been saved'}
    
