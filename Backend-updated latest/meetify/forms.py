from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_login import current_user
from wtforms.validators import DataRequired, Email, EqualTo, Length, email_validator,email, ValidationError
from meetify.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])

	confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	
	submit= SubmitField('Sign Up') 

	def validate_username(self, username):
	 
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username Already Exists')


	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('E-mail Already Exists')

	
	

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

	
	submit= SubmitField('Update') 

	def validate_username(self, username):
		if username.data!=current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username Already Exists')


	def validate_email(self, email):
    	if email.data!=current_user.email:
    		user=User.query.filter_by(email=email.data).first()
		    if user:
			    raise ValidationError('E-mail Already Exists')