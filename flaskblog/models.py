from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    subscriber_id = db.Column(db.Integer, db.ForeignKey(
            'user.id'), nullable=False)
    subscribed_to_id = db.Column(db.Integer, db.ForeignKey(
            'user.id'), nullable=False)    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.String(20))
    image_file = db.Column(db.String(255), nullable = False, default='default.jpg')  
    password = db.Column(db.String(60), nullable = False)
    bio = db.Column(db.String(350))
    posts = db.relationship('Post', backref = 'author', lazy = True)
    date_registered = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    pdf_url = db.Column(db.String(200))
    subscribers = db.relationship('Subscription', foreign_keys=[Subscription.subscribed_to_id], backref=db.backref('subscriber'))
    subscribed_to = db.relationship('Subscription', foreign_keys=[Subscription.subscriber_id], backref=db.backref('subscribed_to'))

    @property
    def num_subscribers(self):
        return self.subscribers.count('subscribers')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):      
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    media = db.Column(db.String(200))
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    original_filename = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))
     