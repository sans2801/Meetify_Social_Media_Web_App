from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

from flask_mail import Mail, Message
import random



app = Flask(__name__)
app.config['SECRET_KEY'] = '7dca0e88733cd8de2233d9759a36fa24'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column( db.Integer, primary_keys = True)
    username = db.Column( db.String(20), unique = True, nullable = False)
    email = db.Column( db.String(120),unique = True, nullable = False)
    image_file = db.Column( db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column( db.String(60),nullable = False)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
        

@app.route('/')
def home():
    return 'Home page'

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form =form)

@app.route('/signup')
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', form= form)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

if __name__ == "__main__":
    app.run(debug = True)