from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, email_validator,email, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit= SubmitField('Sign Up')

    

class LoginForm(FlaskForm):
     email = StringField('Email', validators=[DataRequired(), Email()])
     password = PasswordField('Password', validators=[DataRequired()])
     submit= SubmitField('Login')




class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordResetForm(FlaskForm):
    current_password = PasswordField('Password', validators=[DataRequired()])

