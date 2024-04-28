from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from flask_login import login_required
from PupAdoption import engine
from PupAdoption.pup_models import Puppy
from PupAdoption.puppies.forms import AddForm, DelForm

puppies_blueprints = Blueprint('puppies', __name__, template_folder='templates/puppies')

@puppies_blueprints.route('/add', methods=['GET', 'POST'])
@login_required
def add_pup():
    aform = AddForm()
    if aform.validate_on_submit():
        name = aform.name.data
        new_pup = Puppy(name)
        with Session(engine) as session:
            session.add(new_pup)
            session.commit()
        flash("Puppy %s - Successfully added!" % name)
        return redirect(url_for('puppies.add_pup'))
    return render_template('add.html', form = aform)

@puppies_blueprints.route('/list')
@login_required
def list_pup():
    with Session(engine) as session:  
        puppies = session.query(Puppy).all()
        return render_template('list.html', puppies=puppies)
    
@puppies_blueprints.route('/delete', methods=['GET', 'POST'])
@login_required
def del_pup():
    dform = DelForm()
    if dform.validate_on_submit():
        id = dform.id.data
        with Session(engine) as session:
            rm_pup = session.query(Puppy).filter_by(id=id).one_or_none()
            session.delete(rm_pup)
            session.commit()
        flash("Puppy with ID %s - Successfully deleted!!" % id)
        return redirect(url_for('puppies.del_pup'))
    return render_template('del.html', form = dform)
