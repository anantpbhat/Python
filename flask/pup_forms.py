from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = StringField('Name of the Puppy: ')
    owner = StringField('Owner Name: ')
    toys = StringField("Puppy's Toy items: ")
    submit = SubmitField('Add Puppy')

class DelForm(FlaskForm):
    id = IntegerField("ID number of the Puppy to be removed: ")
    submit = SubmitField('Delete Puppy')
