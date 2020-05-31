from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_socketio import SocketIO
import random



app = Flask(__name__)
app.config['SECRET_KEY'] = '7dca0e88733cd8de2233d9759a36fa24'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = SQLAlchemy(app)
socketio=SocketIO(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)


from meetify import routes