from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from PupAdoption.pup_models import User
from PupAdoption import engine
from PupAdoption.users.forms import LoginForm, RegistrationForm
from sqlalchemy.orm import Session

users_blueprints = Blueprint('users', __name__, template_folder='templates/users')

@users_blueprints.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')

@users_blueprints.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out!!")
    return redirect(url_for('home'))

@users_blueprints.route('/login', methods=['GET', 'POST'])
def login():
    lform = LoginForm()
    if lform.validate_on_submit():
        with Session(engine) as session:
            user = session.query(User).filter_by(email=lform.email.data).first()
            if user.check_password(lform.passwd.data) and user is not None:
                login_user(user)
                flash('%s - Logged in Successfully!' % user.username)
                nextpg = request.args.get('next')
                if nextpg == None or not nextpg[0] == '/':
                    nextpg = url_for('users.welcome_user')
                return redirect(nextpg)
    return render_template('login.html', form=lform)

@users_blueprints.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        user = User(email=rform.email.data, 
                    username=rform.username.data, 
                    passwd=rform.passwd.data)
        #rform.check_email(user.email)
        #rform.check_username(user.username)
        with Session(engine) as session:
            session.add(user)
            session.commit()
            flash("User %s - Registered Successfully!!" % user.username)
        return redirect(url_for('users.login'))
    return render_template('register.html', form=rform)
