from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, SearchForm)
from flaskblog.users.utils import save_picture, send_reset_email
from flask_wtf.csrf import generate_csrf
from sqlalchemy import and_
from flask_jwt_extended import create_access_token

users = Blueprint('users', __name__)

@users.route("/register", methods=['POST'])    
def register():
    if current_user.is_authenticated:
        return jsonify({'message': 'User already logged in'}), 403

    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # You'd validate data here

    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=password)
    access_token = create_access_token(identity=email)
    db.session.add(user)
    db.session.commit()
    # login_user(user, remember=True)
    return jsonify({'message': 'Account created successfully', 'access_token': access_token, 'username': user.username, 'user_id': user.id}), 201

@users.route("/login", methods=['POST'])    
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'User already logged in'}), 403

    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and password == user.password:
        
    # if user and bcrypt.check_password_hash(user.password, password):
        # login_user(user, remember=True)
        access_token = create_access_token(identity=email)
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'username': user.username, 'user_id': user.id, 'phone': user.phone}), 200
    else:    
        return jsonify({'message': 'Login unsuccessful. Please check email and password'}), 401

@users.route("/page/<int:user_id>", methods=['GET'])
def users_page(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)  # Return a 404 Not Found if the user doesn't exist
    posts = Post.query.filter_by(author=user).all()
    return render_template('user_page.html', user=user, posts=posts)

@users.route("/phone/<int:user_id>", methods=['PUT'])
def add_phone(user_id):
    data = request.json
    phone = data.get('phone')

    user = User.query.filter_by(id=user_id).first()
    if user and phone:
        user.phone = phone
        db.session.commit()
        return jsonify({'message': 'Phone number added successfully'}), 200
    elif not phone:
        return jsonify({'message': 'Phone number is missing'}), 400
    else:
        return jsonify({'message': "User with this id doesn't exist"}), 404
    

# @users.route("/logout")   
# def logout():
#     logout_user()
#     return jsonify({'message': 'User logged out successfully'}), 200

# @users.route("/account", methods=['GET', 'POST'])  
# @login_required 
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             image = request.files["picture"]
#             picture_file = save_picture(image)
#             current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.bio = form.bio.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('YOUR ACCOUNT HAS BEEN UPDATED!', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.bio.data = current_user.bio
#         form.email.data = current_user.email
#     image_file = current_user.image_file
#     return render_template('account.html', title='ACCOUNT', image_file=image_file, form=form) 

# @users.route("/user/<string:username>")
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_posts.html', posts=posts, user=user)           

# @users.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RequestResetForm()    
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('AN EMAIL HAS BEEN SENT WITH INSTRUCTIONS TO RESET YOUR PASSWORD', 'info')
#         return redirect(url_for('users.login'))
#     return render_template('reset_request.html', title='RESET PASSWORD', form=form)        

# @users.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))  
#     user = User.verify_reset_token(token) 
#     if user is None:
#         flash('THAT IS AN INVALID OR EXPIRED TOKEN', 'warning')     
#         return redirect(url_for('users.reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash(f'YOUR PASSWORD HAS BEEN UPDATE! YOU ARE NOW ABLE TO LOG IN', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('reset_token.html', title='RESET PASSWORD', form=form)    

# @users.route('/profile/<string:username>', methods=['GET', 'POST'])
# def profile(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5) 

#     return render_template('profile.html', user=user, posts=posts)

# @users.route('/subscribe/<string:username>', methods=['GET', 'POST'])
# @login_required
# def subscribe(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     subscription = Subscription.query.filter_by(subscriber_id=current_user.id, subscribed_to_id=user.id).first()

#     if subscription:
#         db.session.delete(subscription)
#         db.session.commit()
#     else:
#         new_subscription = Subscription(subscriber_id=current_user.id, subscribed_to_id=user.id)
#         db.session.add(new_subscription)
#         db.session.commit()

#     return redirect(url_for('users.profile', username=username))  
    
# @users.route('/message/notification', methods=['GET'])
# def notification():
#     user = User.query.filter_by(username=current_user.username).first_or_404()

#     logged_in_user_subscriptions = Subscription.query.join(User, and_(
#             Subscription.subscriber_id == current_user.id,
#             Subscription.subscribed_to_id == User.id
#             )).all()       
#     logged_in_user_comments = Comment.query.join(Post).filter(Post.author == current_user).all()
#     logged_in_user_likes = Like.query.join(Post).filter(Post.author == current_user).all()

#     return render_template('notification.html', user=user, logged_in_user_subscriptions=logged_in_user_subscriptions,
#                            logged_in_user_comments=logged_in_user_comments, logged_in_user_likes=logged_in_user_likes)                           

# @users.context_processor
# def base():
#     form = SearchForm()
#     return dict(form=form)

# @users.route('/search', methods=['GET', 'POST'])
# def search():           
#     form = SearchForm()
#     search_results = []

#     if request.method == 'POST':
#         if form.validate_on_submit():
#             searched = form.searched.data
#             search_results = User.query.filter(
#                 User.username.ilike(f'%{searched}%'),
#             ).all()
#             return render_template('search.html', form=form, search_results=search_results)    
#         else:    
#             pass
#     return render_template('search.html', form=form)