from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, email_validator,email, ValidationError
from meetify.models import User
from meetify.mongodbOperations import *


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit= SubmitField('Sign Up') 

    def check_user(username):
        return user_collection.count_documents({'username':username})
        
    def check_email(email):
        return user_collection.count_documents({'email':email})

    
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Login')




class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordResetForm(FlaskForm):
    current_password = PasswordField('Password', validators=[DataRequired()])

class UpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    
    
    
    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','webp'])])

    interests=StringField('Interests',validators=[DataRequired()])

    submit= SubmitField('Update Profile') 

    def validate_username(self, username):
        if username.data!=current_user.username:
            user=user_collection.count_documents({'username':username.data})
            if user:
                raise ValidationError('Username Already Exists')


    def validate_email(self, email):
        if email.data!=current_user.email:
            user=user_collection.count_documents({'email':email.data})
            if user:
                raise ValidationError('E-mail Already Exists')