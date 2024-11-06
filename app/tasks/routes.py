from flask import render_template, request, jsonify, redirect, url_for, flash
from app import db
from app.tasks import bp
from app.tasks.models import Task, BaseTask, UserTask
from app.tasks.forms import AddTaskForm, GetPostForm
from flask_login import login_required, current_user
from app.admins.models import Admin
import json
from app.users.forms import AddInstagramForm
from datetime import datetime


@bp.route('/', methods=['GET'])
@login_required
def tasks():
    if current_user.admin:
        admin = Admin.get_by_user_id(current_user.id)
        shop = admin.current_shop
        return render_template('admin_tasks.html', tasks=shop.tasks, admin=admin)
    else:
        from app.shops.models import Shop
        tasks = [task for task in Task.query.filter_by(status='Active').all() 
         if any(usertask.user == current_user for usertask in task.usertasks)]
        # tasks=Task.query.filter_by(status='Active').all()
        # for task in tasks:
        #     if task.usertasks:
        #         for usertask in task.usertasks:
        #             if usertask.user == current_user:
        #                 tasks.remove(task)
        return render_template('users_tasks.html', tasks=tasks, user=current_user, add_instagram_username_form_url=url_for('users.add_instagram_username', _external=True), activate_telegram_bot=url_for('users.activate_tg_bot', _external=True))


@bp.route('/find_task', methods=['GET', 'POST'])
@login_required
def find_task():
    tasks = [task for task in Task.query.filter_by(status='Active').all() 
         if not any(usertask.user == current_user for usertask in task.usertasks)]
    print('tasks: ', tasks)
    return render_template('tasks.html', tasks=tasks, user=current_user)

@bp.route('/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task_card(task_id):
    task = Task.get(task_id)
    if current_user.admin:
        admin = Admin.get_by_user_id(current_user.id)
        return render_template('task_card.html', task=task, admin=admin)
    else:
        usertask = UserTask.query.filter_by(user_id=current_user.id, task_id=task_id).first()
        return render_template('task.html', task=task, user=current_user, usertask=usertask)

@bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    admin = Admin.get_by_user_id(current_user.id)
    shop_id = admin.current_shop_id
    from app.shops.models import Shop
    shop = Shop.query.get(shop_id)

    form = AddTaskForm(formdata=request.form)
    if form.admin_id.data is None:
        if request.args.get('basetask_id') == '1':
            form.update(admin_id=admin.id, shop_id=shop_id, task_selected=request.args.get('basetask_id'), task_selected_name=request.args.get('name'))
        else:
            form.update(admin_id=admin.id, shop_id=shop_id, task_selected=request.args.get('basetask_id'), task_selected_name=BaseTask.query.get(request.args.get('basetask_id')).name)


    if request.method == 'POST': 
        print('post request: ', request.form)
        print('form data: ', form.data)
        if form.validate_on_submit():
            print('the form is validated')
            print('form entries: ', form.posts.entries)
            print('posts data: ', form.posts.data) # form.posts.data
            print('form posts:', form.posts)

            selected_posts = [post.shortcode.data for post in form.posts if post.selected.data]
            print('selectedposts: ', selected_posts)


            from app.instagram.models import InstagramPost            

                    
            # for key, value in request.form.items():
            #     if key.startswith('posts-') and key.endswith('-selected') and value == 'y':
            #         post_id = key.split('-')[1]
            #         form.posts.entries[post_id].shortcode.data = request.form[f'posts-{post_id}-shortcode']
            #         form.posts.entries[post_id].id.data = request.form[f'posts-{post_id}-id']
            posts = [InstagramPost.query.filter_by(shortcode=shortcode).first() for shortcode in selected_posts]
            if len(posts) > 0:
            
                task = Task.add(
                    basetask_id=form.task_selected.data,
                    name = form.task_selected_name.data,
                    points=form.points_input.data,
                    max_rewards = form.rewards_input.data,
                    total_points = int(form.points_input.data) * int(form.rewards_input.data),
                    shop_id=form.shop_id.data,
                    onetime=form.onetime.data,
                    only_followers=form.only_followers.data,
                    checking_type=form.checking_type.data,
                    ai_conditions=form.ai_conditions.data, 
                    posts=posts,
                    five_words=form.five_words.data,
                    description=form.description.data
                    )
                print('new task: ', task.id)
                flash('Task added, but not activated', 'success')
                return redirect(url_for('tasks.tasks'))
            else:
                flash('No posts selected', 'danger')
        else:
            print(form.errors)

    print('form data: ', form.data)
    return render_template('add_task.html', form=form, shop=shop)


@bp.route('/tasks/add_task/post_selected/<int:post_id>', methods=['POST'])
@login_required
def post_selected(post_id):
    print('post selected request: ', request.form)
    form = AddTaskForm(formdata=request.form)
    posts_selected = []
    if form.posts_selected.data:
        posts_selected = form.posts_selected.data.split(',')
    posts_selected.append(post_id)
    form.posts_selected



@bp.route('/add_task/success/<int:task_id>', methods=['GET'])
@login_required
def added_success(task_id):
    task = Task.get(task_id)
    return render_template('added_success.html', task=task, user=current_user)

@bp.route('/checking_type_changed', methods=['POST'])
@login_required
def checking_type_changed():
    if request.form.get('checking_type') == 'AI' or request.form.get('checking_type') == 'AI+Manual':
        form = AddTaskForm(request.form)
        return render_template('ai_conditions_form.html', form)
    else:
        return ''
    
@bp.route('add_basetask/<string:name>', methods=['GET', 'POST'])
@login_required
def add_basetask(name):
    basetask = BaseTask(name=name)
    db.session.add(basetask)
    db.session.commit()
    return jsonify({})

@bp.route('/get_posts', methods=['GET', 'POST'])
@login_required
def get_posts():
    print('add posts request: ', request.form)
    from app.shops.models import Shop
    from app.tasks.forms import AddTaskForm
    form = AddTaskForm(request.form)
    shop = Shop.query.get(form.shop_id.data)
    posts = shop.get_and_update_posts()
    form.update_posts(posts)
    return render_template('/add_task_comment_form_posts.html', form=form, shop=shop)


@bp.route('/activate/<int:task_id>', methods=['GET'])
@login_required
def activate(task_id):
    task = Task.get(task_id)
    if current_user.points >= task.total_points:
        return render_template('task_activate.html', task=task)
    else:
        return render_template('not_enough_points.html')
    

@bp.route('/activate_submit/<int:task_id>', methods=['GET'])
@login_required
def activate_submit(task_id):
    task = Task.get(task_id)
    admin = Admin.get_by_user_id(current_user.id)
    if current_user.points >= task.total_points:
        task.status = 'Active'
        admin.block_points(points=task.total_points, reason='Activated task', task_id=task_id)
        current_user.add_points(points=-task.total_points, reason='Activated task', task_id=task_id)
        db.session.commit()
        flash('Task activated', 'success')
        return redirect(url_for('tasks.tasks'))


@bp.route('/pause/<int:task_id>', methods=['GET'])
@login_required
def pause(task_id):
    task = Task.get(task_id)
    task.status = 'Paused'
    db.session.commit()
    return redirect(url_for('tasks.tasks'))


@bp.route('/delete/<int:task_id>', methods=['GET'])
@login_required
def delete(task_id):
    task = Task.get(task_id)
    task.delete()
    return redirect(url_for('tasks.tasks'))


@bp.route('/usertasks', methods=['GET'])
@login_required
def usertasks():
    if not current_user.admin:
        usertasks = UserTask.query.filter_by(user_id=current_user.id).all()
        for usertask in usertasks:
            print('usertask: ', usertask)
            print('status: ', usertask.status)
            print('task: ', usertask.task)

        return render_template('users_tasks.html', tasks=usertasks, user=current_user)
    else:
        admin = Admin.get_by_user_id(current_user.id)
        tasks = admin.current_shop.tasks
        pass

@bp.route('/usertasks/<int:task_id>', methods=['GET'])
@login_required
def task_usertasks(task_id):
    task = Task.get(task_id)
    usertasks = task.usertasks
    admin = Admin.get_by_user_id(current_user.id)
    return render_template('task_usertasks.html', usertasks=usertasks, task=task, admin=admin)


@bp.route('/usertask/<int:usertask_id>', methods=['GET'])
@login_required
def usertask(usertask_id):
    usertask = UserTask.query.get(usertask_id)
    task = usertask.task
    if not current_user.admin:
        return render_template('usertask.html', task=task, user=current_user, usertask=usertask)
    else:
        admin = Admin.get_by_user_id(current_user.id)
        return render_template('task_usertasks.html', task=task, admin=admin, usertasks=[usertask])


@bp.route('/start_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def start_task(task_id):
    task = Task.get(task_id)
    if task.status == 'Active' and current_user.usertasks not in task.usertasks:
        if current_user.points >= task.price:
            task.start(current_user)
    return redirect(url_for('tasks.usertasks'))

@bp.route('/send_to_manual_checking/<int:usertask_id>', methods=['GET', 'POST'])
@login_required
def send_to_manual_checking(usertask_id):
    usertask = UserTask.query.get(usertask_id)
    usertask.waiting_for_check()
    return redirect(url_for('tasks.usertasks'))
    

@bp.route('/finish_task/<int:usertask_id>', methods=['GET', 'POST'])
@login_required
def finish_task(usertask_id):
    usertask = UserTask.query.get(usertask_id)
    task = usertask.task
    print('task name: ', task.name)
    if task.basetask.id == 1:  
        from app.instagram.models import Instagram, Comment
        instagram = Instagram(task.shop.instagram_token)

        # shop_profile = instagram.download_profile(task.shop.instagram_username)
        # shop_profile = instagram.get_profile(task.shop.instagram_username)
        # if shop_profile:
        #     print('shop profile loaded: ', shop_profile.username)
        for post in task.posts:
            comments = instagram.get_comments(post.id)
            if comments:
                print('comments loaded: ', comments)
                for comment in comments:
                    if comment['from']['username']== current_user.instagram_page.username:
                        print('found comment: ', comment['text'])
                        c = Comment.query.get(comment['id'])
                        if not c:
                            c = Comment.add(id=comment['id'], post_id=post.id, owner_id=comment['from']['id'], text=comment['text'], timestamp=comment['timestamp'], usertask=usertask)
            
    check_response = task.check_conditions(current_user, usertask)
    print('check response: ', check_response)
    if task.ai_conditions:
        ai_response = usertask.check_comment_ai(usertask.comment.text)
        if ai_response is not True:
            check_response.append({'ai_response': ai_response})
    if check_response == True:
        usertask.finish()
        if task.checking_type == 'Manual check':
            usertask.waiting_for_check()
            flash ('The task has been sent for manual checking by admin', 'success')
        elif task.checking_type == 'Auto check':
            usertask.submit()
    #TODO: Finish task
    else:
        conditions = ''
        for response in check_response:
            if conditions != '':
                conditions = conditions + ', ' + response
            else:
                conditions = response
        usertask.reject(rejected_reason=conditions)
        flash('The task was rejected. Conditions not met: {}'.format(conditions), 'error')
    
    return redirect(url_for('tasks.usertasks'))


@bp.route('/claim_reward/<int:usertask_id>', methods=['GET', 'POST'])
@login_required
def claim_reward(usertask_id):
    usertask = UserTask.query.get(usertask_id)
    usertask.claim_reward()
    return redirect(url_for('tasks.usertasks'))


@bp.route('/submit_task/<int:usertask_id>', methods=['GET', 'POST'])
@login_required
def submit_task(usertask_id):
    usertask = UserTask.query.get(usertask_id)
    usertask.submit()
    flash ('Task submitted', 'success')
    return redirect(url_for('tasks.usertasks', task_id=usertask.task.id))


@bp.route('/reject/<int:usertask_id>', methods=['GET', 'POST'])
@login_required
def reject(usertask_id):
    usertask = UserTask.query.get(usertask_id)
    from app.tasks.forms import RejectTaskForm
    form = RejectTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            usertask.reject(rejected_reason=form.reason.data)
            flash('The task was rejected', 'success')
            redirect(url_for('tasks.usertasks', task_id=usertask.task.id))
    return redirect(url_for('tasks.usertasks'))


@bp.route('/refuse/<int:usertask_id>', methods=['GET', 'POST'])
@login_required
def refuse(usertask_id):
    usertask = UserTask.query.get(usertask_id)
    usertask.refuse()
    return redirect(url_for('tasks.usertasks'))