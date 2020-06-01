from time import localtime,strftime
import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from meetify import app,db,bcrypt,socketio
from meetify.forms import RegistrationForm, LoginForm, UpdateAccountForm
from meetify.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit,join_room,leave_room
from meetify.mongodbOperations import *


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

@app.route('/discussionForum',methods=['GET','POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please Login','danger')
        return redirect(url_for('login'))

    return render_template('discussionForum.html',username=current_user.username)


@app.route('/chat_page/<room_id>',methods=['GET','POST'])
def chat_page(room_id):

    if not current_user.is_authenticated:
        flash('Please Login','danger')
        return render_template(url_for('login'))

    room=get_room(room_id)
    messages=get_messages(room_id)

    return render_template('chat_page.html',username=current_user.username,room=room,messages=messages)



@app.route('/create_room',methods=['GET','POST'])
@login_required
def create_room():
    message=''
    if request.method=='POST':
        room_name=request.form.get('room_name')
        usernames=[username.strip() for username in request.form.get('members').split(',')]
        
        if len(room_name) and len(usernames):
            room_id=save_room(room_name,current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)

            add_room_members(room_id,room_name,usernames,current_user.username)
            return redirect(url_for('groups'))
    
        else:
            message='Please enter required fields'

    return render_template('create_room.html',message=message)



@app.route('/grp_page/<room_id>')
@login_required
def grp_page(room_id):
    room=get_room(room_id)
    return render_template('grp_page.html',room=room)


@app.route('/groups')
@login_required
def groups():
    rooms=get_rooms_for_user(current_user.username)
    return render_template('groups.html',rooms=rooms)


@app.route('/join_groups')
@login_required
def join_groups():
    return render_template('join_groups.html')
    


#----------------Old Socket Events--------------------------------------------------------------

@socketio.on('message')
def message(data):
    print(f'\n\n{ data }\n\n')
    save_message(data['room'],data['msg'],data['username'])
    send({'msg':data['msg'],'username':data['username'],'time_stamp':strftime('%b-%d %I:%M%p',localtime())},room=data['room'])


@socketio.on('join')
def join(data):
    join_room(data['room'])
    emit( 'joining_event',{'msg':(data['username']+" is online")},room=data['room'])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    emit('leaving_event',{'msg':(data['username']+" went offline")},room=data['room'])
#-------------------------------------------------------------------------------------------------

