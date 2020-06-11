from time import localtime,strftime
from bson import ObjectId
import os
import secrets
import pymongo
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from meetify import app,bcrypt,socketio,login_manager
from meetify.forms import RegistrationForm, LoginForm, UpdateAccountForm
from meetify.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit,join_room,leave_room
from meetify.mongodbOperations import *
from cloudinary.uploader import upload
from cloudinary import CloudinaryImage

interests=['Technology','Photography','Dance','Singing','College Life','Competitive exams']


##############################################################################################
@app.route('/')
@app.route('/home')
def home():
    return render_template('HomePage.html')

##############################################################################################

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()	
    if form.validate_on_submit():
        user=get_user_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user['password'],form.password.data):
            
            login_user(User(user['username'],user['email'],user['password'],user['image_file'],user['interests']))
            return redirect(url_for('dashboard'))
        else:
            flash('please check your credentials', 'danger')
    return render_template('login.html', form =form)
##################################################################################################


##################################################################################################

@app.route('/user',methods=['GET','POST'])
@login_required
def user():
 
    form=UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            imageDict=upload(form.picture.data)
            user_collection.update_one({'username':current_user.username},{'$set':{'image_file':imageDict['url']}})
        
        username=form.username.data
        email=form.email.data
        new_interests=request.form.getlist('interests')

        if user_collection.count_documents({'username':username}):
            flash("username is taken")
            user_collection.update_one({'username':current_user.username},{'$set':{'email':email,'interests':new_interests}})
            return render_template('user.html', form=form)

        if user_collection.count_documents({'email':email}):
            flash("email is taken, please login again")
            user_collection.update_one({'username':current_user.username},{'$set':{'username':username,'interests':new_interests}})
            return redirect(url_for('login'))



        user_collection.update_one({'username':current_user.username},{'$set':{'username':username,'email':email,'interests':new_interests}})
        flash('Your account has been updated, please login again')
        return redirect(url_for('login'))

    elif request.method=='GET':
	    form.username.data=current_user.username
	    form.email.data=current_user.email

    image_file=url_for('static',filename='profilepics/'+current_user.image_file)
    return render_template('user.html', form=form,curr_interests=current_user.interests,curr_pic=current_user.image_file,interests=interests)

##########################################################################################

@app.route('/signup',methods=['GET','POST'])
def signup():	
    if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    
    
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        save_user(form.username.data,form.email.data,hashed_password,'none')

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form= form)

#########################################################################################    

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

#########################################################################################

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

##########################################################################################

@app.route("/dashboard")
@login_required
def dashboard():
    image_file=url_for('static',filename='profilepics/'+current_user.image_file)
    return render_template('dashboard.html')

###########################################################################################

@app.route('/map')
@login_required
def map():
    return render_template('map.html')

############################################################################################

@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

#############################################################################################

@app.route('/discussionForum',methods=['GET','POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please Login','danger')
        return redirect(url_for('login'))

    return render_template('discussionForum.html',username=current_user.username)

#############################################################################################

@app.route('/chat_page/<room_id>',methods=['GET','POST'])
def chat_page(room_id):

    if not current_user.is_authenticated:
        flash('Please Login','danger')
        return redirect(url_for('login'))

    if is_room_member(room_id,current_user.username):
        room=get_room(room_id)
        messages=get_messages(room_id)

        return render_template('chat_page.html',username=current_user.username,room=room,messages=messages)
    else:
        return redirect(url_for('groups'))
###############################################################################################

@app.route('/create_room',methods=['GET','POST'])
@login_required
def create_room():
    message=''
    if request.method=='POST':
        room_name=request.form.get('room_name')
        usernames=[username.strip() for username in request.form.get('members').split(',')]
        room_interests=request.form.getlist('room_interests')
        tags=[tag.strip() for tag in request.form.get('tags').split(',')]
        status=request.form.get('status')

        for username in usernames:
            

            if not user_collection.count_documents({'username':username}):
                flash(f"Invalid username: { username }")
                return redirect(url_for('create_room'))

        tags=tags+room_interests

        
        if room_name and usernames:
            room_id=save_room(room_name,current_user.username,tags,status)
            if current_user.username in usernames:
                usernames.remove(current_user.username)

            if not usernames:
                return redirect(url_for('groups'))
            else:
                add_room_members(room_id,room_name,usernames,current_user.username)
            
            return redirect(url_for('groups'))
    
        else:
            flash('Please enter required fields')

    return render_template('create_room.html',interests=interests)

###############################################################################################

@app.route('/grp_page/<room_id>',methods=['GET','POST'])
@login_required
def grp_page(room_id):
    room=get_room(room_id)
    isAdmin=is_room_admin(room_id,current_user.username)
    members=get_room_members(room_id)
    isMember=is_room_member(room_id,current_user.username)



    if request.method=='POST':

        username=request.form.get('add_member')
        username2=request.form.get('remove_member')

        if (username and username2) or username:

            if not len(username):
                flash(f"please enter some values")
                return render_template('grp_page.html',room=room,isAdmin=isAdmin,members=members,isMember=isMember)

            
            user=user_collection.count_documents({'username':username})
            if not user:
                flash(f"Invalid username: { username }")
                return render_template('grp_page.html',room=room,isAdmin=isAdmin,members=members,isMember=isMember)
                    

            if is_room_member(room_id,username):
                flash(f"{ username } is already a participant")
                return render_template('grp_page.html',room=room,isAdmin=isAdmin,members=members,isMember=isMember)

                
            add_room_member(room_id,room['room name'],username,current_user.username)
            flash(f"Added Succesfully")

        if (username and username2) or username2:
            
            if not len(username2):
                flash(f"please enter some values")
                return render_template('grp_page.html',room=room,isAdmin=isAdmin,members=members,isMember=isMember)

            if not is_room_member(room_id,username2):
                flash(f"{ username2 } is not a participant")
                return render_template('grp_page.html',room=room,isAdmin=isAdmin,members=members,isMember=isMember)

            if username2==current_user.username:
                flash("You can't remove yourself, leave instead")
                return render_template('grp_page.html',room=room,isAdmin=isAdmin,members=members,isMember=isMember)


            remove_room_member(room_id,username2)
            flash(f"{ username2 } was succesfully removed")


        
    return render_template('grp_page.html',room=room,isAdmin=isAdmin,members=members,isMember=isMember)

@app.route('/grp_page/leave/<username>/<room_id>')
@login_required
def leave_grp(username,room_id):

    room=get_room(room_id)
    if (is_room_admin(room_id,current_user.username)):
        members=get_room_members(room_id)
        if len(members)==1:
            remove_room_member(room_id,username)
            messages_collection.delete_many({'room_id':room_id})
            rooms_collection.delete_one({'_id':ObjectId(room_id)})

        else:
            members[1]['is_room_admin']=True

    remove_room_member(room_id,username)
    flash(f"Succesfully left { room['room name'] }")
    return redirect(url_for('groups'))

################################################################################################

@app.route('/groups')
@login_required
def groups():
    rooms=get_rooms_for_user(current_user.username)
    return render_template('groups.html',rooms=rooms)

################################################################################################

@app.route('/join_groups',methods=['GET','POST'])
@login_required
def join_groups():
    recommended_rooms=get_room_with_tags(current_user.interests)
    if request.method=='POST':
        grp_info=request.form.get('grp_name')

        if not grp_info:
            flash("please fill the required fields(s)")
            return render_template('join_groups.html',recommended_rooms=recommended_rooms)

        grp_info=[word.strip() for word in grp_info.split(' ')]
        rooms=list(rooms_collection.find({
            '$or':[
            {'$or':[{'room name':{'$regex':word,'$options':'i'}}for word in grp_info]},
            {'$or':[{'tags':{'$regex':word,'$options':'i'}}for word in grp_info]},
            {'$or':[{'created by':{'$regex':word,'$options':'i'}}for word in grp_info]}
            ]})
        )

        if rooms==[]:
            flash("No Groups Found")

        return render_template('join_groups.html',recommended_rooms=recommended_rooms,rooms=rooms)
            
    return render_template('join_groups.html',recommended_rooms=recommended_rooms)
    

@app.route('/join_group/<room_id>')
@login_required
def join_group(room_id):
    room=get_room(room_id)

    if is_room_member(room_id,current_user.username):
        flash(f"{current_user.username} is already in {room['room name']}")
        return redirect(url_for('join_groups')) 

    else:
        add_room_member(room_id,room['room name'],current_user.username,'joined')
        flash(f"{current_user.username} has joined {room['room name']} !!")
        return redirect(url_for('groups')) 

    return render_template('join_groups.html',recommended_rooms=recommended_rooms)




@login_manager.user_loader
def load_user(username):
    user=get_user(username)
    if user:
        return User(user['username'],user['email'],user['password'],user['image_file'],user['interests'])
    else:
        return None 


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

