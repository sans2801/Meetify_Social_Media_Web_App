from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_socketio import SocketIO
import random
import cloudinary as Cloud

app = Flask(__name__)
app.config['SECRET_KEY'] = '7dca0e88733cd8de2233d9759a36fa24'
app.config['CLOUDINARY_URL']='cloudinary://832194865169637:i7fVVmebBy-FIG1BUSqmFpaOAaU@meetify4'
socketio=SocketIO(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
Cloud.config(
    cloud_name='meetify4',
    api_key='832194865169637',
    api_secret='i7fVVmebBy-FIG1BUSqmFpaOAaU'
)

from meetify import routes