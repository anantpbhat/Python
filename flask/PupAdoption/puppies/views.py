from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from PupAdoption import db
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
        db.session.add(new_pup)
        db.session.commit()
        flash("Puppy %s - Successfully added!" % name)
        return redirect(url_for('puppies.add_pup'))
    return render_template('add.html', form = aform)

@puppies_blueprints.route('/list')
@login_required
def list_pup():  
    puppies = db.session.execute(db.select(Puppy).order_by(Puppy.id)).scalars()
    return render_template('list.html', puppies=puppies)
    
@puppies_blueprints.route('/delete', methods=['GET', 'POST'])
@login_required
def del_pup():
    dform = DelForm()
    if dform.validate_on_submit():
        id = dform.id.data
        rm_pup = db.one_or_404(db.select(Puppy).filter_by(id=id))
        rm_pup_name = rm_pup.name
        rm_owner = rm_pup.owner
        rm_toys = rm_pup.toys
        print(rm_pup, "\n", rm_owner, "\n", rm_toys)
        db.session.delete(rm_pup)
        if rm_owner:
            db.session.delete(rm_owner)
        if rm_toys:
            for rm_toy in rm_toys:
                db.session.delete(rm_toy)
        db.session.commit()
        flash("Puppy '%s' with ID %s - Successfully deleted!!" % (rm_pup_name, id))
        return redirect(url_for('puppies.del_pup'))
    return render_template('del.html', form = dform)
