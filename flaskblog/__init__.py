import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from dotenv import load_dotenv
# from flask_jwt_extended import JWTManager, create_access_token
import openai
# from flask_cors import CORS
#from flaskblog.posts.s3_utils import upload_to_s3
#from flask_socketio import SocketIO

app = Flask(__name__)
# CORS(app)
load_dotenv()

# app.config['SECRET_KEY'] = "38847e147d716783d82904179bcd7aac"
# app.config['JWT_SECRET_KEY'] = "9332rhhf42h94r8y32741"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

#s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
# jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts

app.register_blueprint(users)
app.register_blueprint(posts)

app.app_context().push() # when initializing the datatabase

# from flaskblog import db
# db.create_all()
# from flaskblog.models import User
# user = User(username='XXXXX', email='XXXXXXXXXXXXXXX', password='XXXXX')
# db.session.add(user)
# db.session.commit()

# flask db init
# flask db migrate -m "Initial commit"
# flask db upgrade