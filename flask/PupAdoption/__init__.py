from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_file = str('sqlite:///' + basedir + '/pup_data.sqlite')
engine = create_engine(db_file, echo=True)

Base = declarative_base()

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

Base.metadata.create_all(engine)

from PupAdoption.puppies.views import puppies_blueprints
from PupAdoption.owners.views import owners_blueprints
from PupAdoption.toys.views import toys_blueprints

app.register_blueprint(puppies_blueprints, url_prefix='/puppies')
app.register_blueprint(owners_blueprints, url_prefix='/owners')
app.register_blueprint(toys_blueprints, url_prefix='/toys')