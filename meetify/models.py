from meetify.mongodbOperations import *

class User:
	def __init__(self,username,email,hashed_password,image_file,interests):
		self.username=username
		self.email=email
		self.hashed_password=hashed_password
		self.image_file=image_file
		self.interests=interests
		
	def get_id(self):
		return self.username
	def is_authenticated():
		return True
	def is_active():
		return True
	def is_anonymous():
		return False
    
    
