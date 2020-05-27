import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from meetify import app,db,bcrypt
from meetify.forms import RegistrationForm, LoginForm, UpdateAccountForm
from meetify.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('HomePage.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()	
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('please check your credentials', 'danger')
    return render_template('login.html', form =form)

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_filename=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/profilepics',picture_filename)
    form_picture.save(picture_path)

@app.route('/user',methods=['GET','POST'])
@login_required
def user(): 
    form=UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('YOur account has been created')
    elif request.method=='GET':
	    form.username.data=current_user.username
	    form.email.data=current_user.email
    image_file=url_for('static',filename='profilepics/'+current_user.image_file)
    return render_template('user.html', form=form)


@app.route('/signup',methods=['GET','POST'])
def signup():	
    if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    
    
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user1)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form= form)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    image_file=url_for('static',filename='profilepics/'+current_user.image_file)
    return render_template('dashboard.html')

@app.route('/map')
@login_required
def map():
    return render_template('map.html')

@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')