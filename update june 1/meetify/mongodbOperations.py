from time import localtime,strftime
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
client=MongoClient()

chat_db=client.get_database("ChatDB")
rooms_collection=chat_db.get_collection("rooms")
room_members_collection=chat_db.get_collection("room_members")
messages_collection=chat_db.get_collection("messages")

def save_room(room_name,created_by):
	room_id=rooms_collection.insert_one({'room name':room_name,'created by':created_by, 'created at':datetime.now()}).inserted_id
	add_room_member(room_id,room_name,created_by,created_by,is_room_admin=True)
	return room_id

def add_room_member(room_id,room_name,username,added_by,is_room_admin=False):
	room_members_collection.insert_one({'_id':{'room_id':ObjectId(room_id),'username':username},'room_name':room_name,
		'added_by':added_by,'added_at':datetime.now(),'is_room_admin':is_room_admin})

def add_room_members(room_id,room_name,usernames,added_by):
	room_members_collection.insert_many([{'_id':{'room_id':ObjectId(room_id),'username':username},'room_name':room_name,
		'added_by':added_by,'added_at':datetime.now(),'is_room_admin':False} for username in usernames])

def get_room(room_id):
	return rooms_collection.find_one({'_id':ObjectId(room_id)})

def get_room_members(room_id):
	return list(room_members_collection.find({'_id.room_id':ObjectId(room_id)}))

def get_rooms_for_user(username):
	return list(room_members_collection.find({'_id.username':username}))

def is_room_member(room_id,username):
	room_members_collection.count_documents({'_id':{'room_id':ObjectId(room_id),'username':username}})

def is_room_admin(room_id,username):
	room_members_collection.count_documents({'_id':{'room_id':ObjectId(room_id),'username':username}, 'is_room_admin':True})

def update_room(room_id,room_name):
	rooms_collection.update_one({'_id':ObjectId(room_id)},{'$set':{'room_name':room_name}})

def remove_room_members(room_id,usernames):
	room_members_collection.delete_many({'_id':{'$in':[{'room_id':room_id,'username':username} for username in usernames ]}})

####################### Messages_Collection Operations###########################################################################

def save_message(room_id,text,sender):
	messages_collection.insert_one({'room_id':room_id ,'text':text,'sender':sender,'created_at':strftime('%b-%d %I:%M%p',localtime())})

def get_messages(room_id):
	return list(messages_collection.find({'room_id':room_id}))