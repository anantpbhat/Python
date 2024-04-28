from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from flask import Flask
from flask_login import LoginManager
import os

Base = declarative_base()

basedir = os.path.abspath(os.path.dirname(__file__))
db_file = str('sqlite:///' + basedir + '/pup_data.sqlite')
engine = create_engine(db_file, echo=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

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

Base.metadata.create_all(engine)