from flask import render_template, url_for, flash, redirect
from meetify import app,db,bcrypt
from meetify.forms import RegistrationForm, LoginForm
from meetify.models import User

@app.route('/')
def home():
	return 'Home page'

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	return render_template('login.html', form =form)

@app.route('/signup',methods=['GET','POST'])
def signup():
	form = RegistrationForm()
	if form.validate_on_submit():

		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user1=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user1)
		db.session.commit()
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('signup.html', form= form)

@app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
	return render_template('forgot_password.html')
