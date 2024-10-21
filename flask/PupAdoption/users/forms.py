from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from PupAdoption.pup_models import User
from PupAdoption import db

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, efield):
        if db.session.execute(db.select(User).filter_by(email=efield)):
            raise ValidationError('This Email is already registered!!')
        return
        
    def check_username(self, ufield):
        if db.session.execute(db.select(User).filter_by(username=ufield)): 
            raise ValidationError('This username is already taken!')
        return
        