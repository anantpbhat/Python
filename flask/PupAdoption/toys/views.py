from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from flask_login import login_required
from PupAdoption import engine
from PupAdoption.pup_models import Toy, Puppy
from PupAdoption.toys.forms import ToyForm

toys_blueprints = Blueprint('toys', __name__, template_folder='templates/toys')

@toys_blueprints.route('/add', methods=['GET', 'POST'])
@login_required
def add_toys():
    tform = ToyForm()
    if tform.validate_on_submit():
        toys = tform.toys.data
        id = tform.id.data
        pup_toys = Toy(toys, id)
        with Session(engine) as session:
            session.add(pup_toys)
            session.commit()
            pup_name = pup_toys.puppy.name
            puppy = Puppy(pup_name)
            flash("Toys '%s' for Puppy %s - Successfully added!" % (toys, pup_name))
        return redirect(url_for('toys.add_toys'))
    return render_template('add_toys.html', form = tform)
