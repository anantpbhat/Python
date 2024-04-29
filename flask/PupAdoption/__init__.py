from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
import os

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

basedir = os.path.abspath(os.path.dirname(__file__))
db_file = str('sqlite:///' + basedir + '/pup_data.sqlite')

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = db_file
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from PupAdoption.puppies.views import puppies_blueprints
from PupAdoption.owners.views import owners_blueprints
from PupAdoption.toys.views import toys_blueprints
from PupAdoption.users.views import users_blueprints

app.register_blueprint(puppies_blueprints, url_prefix='/puppies')
app.register_blueprint(owners_blueprints, url_prefix='/owners')
app.register_blueprint(toys_blueprints, url_prefix='/toys')
app.register_blueprint(users_blueprints, url_prefix='/users')

with app.app_context():
    db.create_all()

#Base.metadata.create_all(engine)