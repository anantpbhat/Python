from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class OwnerForm(FlaskForm):
    owner = StringField('Owner Name: ')
    id = IntegerField("ID number of the Puppy: ")
    submit = SubmitField('Add Owner')
