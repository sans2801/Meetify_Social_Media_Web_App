from time import localtime,strftime
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
#from flask_login import current_user

client=MongoClient("mongodb+srv://test:test@chatdb-vvu54.mongodb.net/ChatDB?retryWrites=true&w=majority")

chat_db=client.get_database("ChatDB")

user_collection=chat_db.get_collection("users")
rooms_collection=chat_db.get_collection("rooms")
room_members_collection=chat_db.get_collection("room_members")
messages_collection=chat_db.get_collection("messages")

################################## User Operations ################################################################################

def save_user(username,email,hashed_password,interests):
	user_collection.insert_one({'username':username,'email':email,'password':hashed_password,'image_file':'http://res.cloudinary.com/meetify4/image/upload/c_scale,w_125/v1591787005/download_jnz2qi.jpg','interests':interests})

def get_user_by_email(email):
	return user_collection.find_one({'email':email})

def get_user(username):
	return user_collection.find_one({'username':username})

def update_user_info(username,email):
	user_collection.update_one({'username':current_user.username},{'$set':{'username':username,'email':email}})


################################### Group Operations ###############################################################################

def save_room(room_name,created_by,tags,status):
	room_id=rooms_collection.insert_one({'room name':room_name,'created by':created_by,'tags':tags, 'status':status, 'created at':datetime.now(), 'profile_pic':'https://res.cloudinary.com/meetify4/image/upload/v1591790336/grpDefault_gkzjob.png' }).inserted_id
	add_room_member(room_id,room_name,created_by,created_by,is_room_admin=True)
	return room_id

def add_room_member(room_id,room_name,username,added_by,is_room_admin=False):
	room_members_collection.insert_one({'_id':{'room_id':ObjectId(room_id),'username':username},'added_by':added_by,'added_at':datetime.now(),'is_room_admin':is_room_admin,'image_file':get_user(username)['image_file']})

def add_room_members(room_id,room_name,usernames,added_by):
	room_members_collection.insert_many([{'_id':{'room_id':ObjectId(room_id),'username':username},'room_name':room_name,
		'added_by':added_by,'added_at':datetime.now(),'is_room_admin':False,'image_file':get_user(username)['image_file']} for username in usernames])

def get_room(room_id):
	return rooms_collection.find_one({'_id':ObjectId(room_id)})

def get_room_members(room_id):
	return list(room_members_collection.find({'_id.room_id':ObjectId(room_id)}))

def get_rooms_for_user(username):
	return list(room_members_collection.find({'_id.username':username}))

def is_room_member(room_id,username):
	return room_members_collection.count_documents({'_id':{'room_id':ObjectId(room_id),'username':username}})

def is_room_admin(room_id,username):
	return room_members_collection.count_documents({'_id':{'room_id':ObjectId(room_id),'username':username}, 'is_room_admin':True})

def update_room(room_id,room_name):
	rooms_collection.update_one({'_id':ObjectId(room_id)},{'$set':{'room_name':room_name}})

def remove_room_members(room_id,usernames):
	room_members_collection.delete_many({'_id':{'$in':[{'room_id':ObjectId(room_id),'username':username} for username in usernames ]}})

def remove_room_member(room_id,username):
	room_members_collection.delete_one({'_id':{'$in':[{'room_id':ObjectId(room_id),'username':username}]}})

def get_room_with_tags(tags):

	if tags=="none":
		return []
	return list(rooms_collection.find({'tags':{'$in':tags}}))

def get_room_with_name(name):
	return list(rooms_collection.find({'room name':name}))

def get_room_with_both(name,tags):
	return list(rooms_collection.find({'$and':[{'room name':name},{'tags':{'$in':tags}}]}))

####################### Messages_Collection Operations###########################################################################

def save_message(room_id,text,sender,image):
	messages_collection.insert_one({'room_id':room_id ,'text':text,'sender':sender,'image':image,'created_at':strftime('%b-%d %I:%M%p',localtime())})

def get_messages(room_id):
	return list(messages_collection.find({'room_id':room_id}))