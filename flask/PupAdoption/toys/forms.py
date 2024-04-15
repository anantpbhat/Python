from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class ToyForm(FlaskForm):
    toys = StringField("Puppy's Toy item/s: ")
    id = IntegerField("ID number of the Puppy: ")
    submit = SubmitField('Add Toy/s')
