from app.instagram import bp
from flask import render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from app.instagram.models import Instagram, InstagramPost, InstagramPage
from app.shops.models import Shop
import os
import requests

# get instagram user data url:
# curl -i -X GET \
#  "https://graph.facebook.com/v21.0/me/accounts?fields=name&access_token=EAAFpjsmwde4BOZBkf4Fg8v2yfawJmxNHrwAJXuZCvBKRrXF2xx5yP3cwYZBblIn5moqZBKdVOYbmzYnHh9Jt91ZBq0B7zDZBmcFNlOFu60mrPOrvxVwPHdeG1AqUGU8tbvZClxq5eliJY92LuXIvTTBn344nCEwM3VX7TfggYD3nlOP9NkKRV14ZBkZC40KZBks1UihNjjvCSz94aT8sr26wZDZD"

# get instagram page data url:
# curl -i -X GET \
#  "https://graph.facebook.com/v21.0/17841456052664713?fields=followers_count%2Cname%2Cprofile_picture_url%2Cwebsite%2Cusername%2Cbiography%2Cmedia_count%2Cmedia&access_token=EAAFpjsmwde4BOwDx2bZA6wCjBOjqD3rC8ZB4GOUZAhm4S64ZCbgkBT6Uya6ZCmE1m7sZA81VlSiD6M7FmOCVg6zSBlDkiuEpR0JhdY3443OpUBH1WaNf0EFz2ADYCNsmcb2FshXbvJL4UROOSqDeawoIZApXumWUw8YUjK7H2laod8xO6YRtdT0LxyYVmK4iE2ZBcKVWD8Kno8KiWOlGZAAZDZD"

# get instagram post data (and comments) url:
# curl -i -X GET \
#  "https://graph.facebook.com/v21.0/17963173018988169/?fields=comments_count%2Ccaption%2Clike_count%2Cmedia_type%2Cowner%2Cmedia_url%2Cpermalink%2Cshortcode%2Cthumbnail_url%2Ctimestamp%2Ccomments%7Bfrom%2Ctext%2Ctimestamp%2Cuser%2Cusername%2Creplies%7D&access_token=EAAFpjsmwde4BOwDx2bZA6wCjBOjqD3rC8ZB4GOUZAhm4S64ZCbgkBT6Uya6ZCmE1m7sZA81VlSiD6M7FmOCVg6zSBlDkiuEpR0JhdY3443OpUBH1WaNf0EFz2ADYCNsmcb2FshXbvJL4UROOSqDeawoIZApXumWUw8YUjK7H2laod8xO6YRtdT0LxyYVmK4iE2ZBcKVWD8Kno8KiWOlGZAAZDZD"

@bp.route('/webhook', methods=['GET'])
def webhook():
    response = request.args.get('hub.challenge')
    return response

@bp.route('/get_posts/<int:page_id>/<string:api_token>', methods=['GET', 'POST'])
@login_required
def get_posts(page_id, api_token):
    page = InstagramPage.query.get(page_id)
    print('instagram_page: ', page)
    i = Instagram(api_token)
    instagram_posts_ids = i.get_instagram_page_posts(page_id)
    print('instagram_posts_ids: ', instagram_posts_ids)
    posts = []
    if instagram_posts_ids:
        for instagram_post_id in instagram_posts_ids:
            post = InstagramPost.query.get(instagram_post_id['id'])
            if not post:
                instagram_post = i.get_post_data(post_id=instagram_post_id['id'])
                post = InstagramPost.add(
                    id=instagram_post['id'], 
                    shortcode=instagram_post['shortcode'], 
                    caption=instagram_post['caption'], 
                    media_type=instagram_post['media_type'],
                    image_url=instagram_post['image_url'],
                    url=instagram_post['url'],
                    page_id=page_id, 
                    timestamp=instagram_post['timestamp']
                )
            posts.append(post)
    return posts

@bp.route('/get_post_image_url/<int:post_id>', methods=['GET'])
def get_post_image_url(post_id):
    
    post = InstagramPost.query.get(post_id)
    shop = Shop.query.get(post.shop_id)
    directory = os.path.join(current_app.config['SHOPS_UPLOAD_DIR'], shop.instagram_username, 'posts')
    image_url = directory + '/' + post.shortcode + '.jpg'
    return send_from_directory(directory=directory, path=image_url)


@bp.route('/get_post_comments/<int:post_id>', methods=['GET'])
def get_post_comments(post_id):
    post = InstagramPost.query.get(post_id)
    if post:
        comments = post.get_comments()
        from app.instagram.models import Comment
        for comment in comments:
            print('comment: ', comment)
            if not Comment.query.get(comment['id']):
                Comment.add(
                    post_id=post.id, 
                    owner_id=comment['from']['id'], 
                    text=comment['text'], 
                    timestamp=comment['timestamp']
                )

        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments