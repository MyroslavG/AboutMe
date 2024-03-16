from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User, Post
from flaskblog.posts.forms import PostForm, CommentForm
import urllib.parse
from sqlalchemy import func, desc
from werkzeug.utils import secure_filename
from flaskblog.s3_utils import upload_to_s3, allowed_file
from flaskblog.users.utils import save_picture
from werkzeug.datastructures import FileStorage
import os
import boto3
import uuid
from flask import app
from flask import jsonify

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['POST'])
@login_required
def new_post():
    title = request.form.get('title')
    content = request.form.get('content')
    media = request.files.get('media')  # Get the file from the request

    if not title or not content:
        return jsonify({'message': 'Missing title or content'}), 400

    uploaded_file_url = None
    if media:
        filename = secure_filename(media.filename)
        uploaded_file_url = save_picture(media)  # Make sure save_picture returns a URL or file path

    post = Post(title=title, content=content, author=current_user, media=uploaded_file_url)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Your post has been created!', 'post': {
        'title': post.title,
        'content': post.content,
        'media': post.media,
    }}), 201


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])  
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, legend='NEW POST')    

# @posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])  
# @login_required
# def update_post(post_id):    
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         if form.media.data: 
#             image = request.files["media"]
#             uploaded_file = save_picture(image)
#             post.media = uploaded_file 
#         db.session.commit()
#         flash('YOUR POST HAS BEEN UPDATED!', 'success')
#         return redirect(url_for('posts.post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='UPDATE POST', form=form, legend='UPDATE POST')  

# @posts.route("/post/<int:post_id>/delete", methods=['POST'])  
# @login_required
# def delete_post(post_id):      
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     likes_to_delete = db.session.query(Like).filter(Like.post_id == post_id).all()
#     for item in likes_to_delete:
#         db.session.delete(item)
#     comments_to_delete = db.session.query(Comment).filter(Comment.post_id == post_id).all()
#     for item in comments_to_delete:
#         db.session.delete(item)

#     db.session.delete(post)
#     db.session.commit()
#     flash('YOUR POST HAS BEEN DELETED!', 'success')
#     return redirect(url_for('main.home'))

# @posts.route('/post/<int:post_id>/like', methods=['POST'])
# @login_required
# def like_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
#     if request.method == 'POST':
#         if (request.form.get('action') == 'increment') and (not like):
#             like = Like(author=current_user.id, post_id=post_id)
#             db.session.add(like)
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 logging.exception(e)
#         elif request.form.get('action') == 'decrement':
#             db.session.delete(like)
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 logging.exception(e)
#         return jsonify({'likes': len(post.likes)})    

# @posts.route('/post/<int:post_id>/comment', methods=['POST'])
# @login_required
# def add_comment(post_id):
#     post = Post.query.get_or_404(post_id)
#     comment_text = request.form.get('comment_text')
#     comment = Comment(text=comment_text, post_id=post.id, author=current_user.id)
#     db.session.add(comment)
#     db.session.commit()
#     return jsonify({'comments': len(post.comments)})

# @posts.route('/post/<int:post_id>/get_comments', methods=['GET'])
# def get_comments(post_id):
#     post = Post.query.get_or_404(post_id)
#     comments_count = len(post.comments)
#     return render_template("comment.html", post=post, comments_count=comments_count)  

# @posts.route('/post/<int:post_id>/comment/<int:comment_id>/delete', methods=['GET', 'POST'])
# @login_required
# def delete_comment(post_id, comment_id):
#     comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first_or_404()
#     if comment.user != current_user:
#         return jsonify({'status': 'error', 'message': 'You are not authorized to delete this comment.'}), 403
    
#     db.session.delete(comment)
#     db.session.commit()
    
#     return jsonify({'status': 'success', 'message': 'Comment deleted successfully.'})    

# @posts.route('/trending')
# def trending():
#     most_liked_posts = db.session.query(
#         Post, func.count(Like.id).label('like_count')
#     ).outerjoin(Like).group_by(Post).order_by(desc('like_count')).all()

#     return render_template('trending.html', posts=most_liked_posts)    

# '''@app.route('/upload_story', methods=['POST'])
# def upload_story():
#     if request.method == 'POST':
#         image_url = request.form['image_url']
#         user_id = 1  # Replace with actual user ID
#         expiration_time = datetime.datetime.now() + datetime.timedelta(hours=24)
#         stories.append({'image_url': image_url, 'user_id': user_id, 'expiration_time': expiration_time})
#         return redirect(url_for('main.home'))'''

# @posts.route('/recommendations')
# @login_required 
# def recommendations():
#     user = current_user  # Get the current logged-in user
#     subscriptions = user.subscribed_to # Assuming you have a relationship named 'subscriptions'
#     recommended_posts = []
#     print(subscriptions)

#     for subscription in subscriptions:
#         recommended_posts.extend(subscription.subscriber.posts)    
#     print(recommended_posts)    

#     return render_template('recommendations.html', posts=recommended_posts)

# @posts.route('/achievements')
# def achievements():           
#     return render_template('achievements.html')   

# @posts.route('/achievements/new', methods=['GET', 'POST'])
# def new_achievement():
#     text = request.form.get('achievement-text')
#     achievement = Achievement(text=text, author=current_user.id)
#     db.session.add(achievement)
#     db.session.commit()
#     return jsonify({'text': text})

# @posts.route('/achievements/update')   
# def update_achievements():
#     #achievements = Achievement.query.filter_by(author=current_user).all()
#     return render_template("achievements_list.html")#, achievements=achievements)