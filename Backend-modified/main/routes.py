from flask import render_template, url_for, flash, redirect
from main import app, db, bcrypt
from main.forms import RegistrationForm, LoginForm
from main.models import User
from flask_mail import Mail, Message
import random



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

