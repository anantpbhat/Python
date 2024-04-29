from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from PupAdoption import db
from PupAdoption.pup_models import Owner
from PupAdoption.owners.forms import OwnerForm

owners_blueprints = Blueprint('owners', __name__, template_folder='templates/owners')

@owners_blueprints.route('/add', methods=['GET', 'POST'])
@login_required
def add_owner():
    oform = OwnerForm()
    if oform.validate_on_submit():
        owner = oform.owner.data
        id = oform.id.data
        pup_owner = Owner(owner, id)
        db.session.add(pup_owner)
        db.session.commit()
        pup_name = pup_owner.puppy.name
        flash("Owner '%s' for Puppy %s - Successfully added!" % (pup_owner.name, pup_name))
        return redirect(url_for('owners.add_owner'))
    return render_template('add_owner.html', form = oform)
