from flask import Flask, render_template, url_for, redirect, flash
from pup_forms import AddForm, DelForm, OwnerForm, ToyForm
from pup_models import engine, Base, Puppy, Owner, Toy
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('pup_home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    aform = AddForm()
    if aform.validate_on_submit():
        name = aform.name.data
        new_pup = Puppy(name)
        with Session(engine) as session:
            session.add(new_pup)
            session.commit()
        flash("Puppy %s - Successfully added!" % name)
        return redirect(url_for('add_pup'))
    return render_template('pup_add.html', form = aform)

@app.route('/owner', methods=['GET', 'POST'])
def owner_pup():
    oform = OwnerForm()
    if oform.validate_on_submit():
        owner = oform.owner.data
        id = oform.id.data
        pup_owner = Owner(owner, id)
        with Session(engine) as session:
            session.add(pup_owner)
            session.commit()
            pup_name = pup_owner.puppy.name
            flash("Owner %s for Puppy %s - Successfully added!" % (pup_owner.name, pup_name))
        return redirect(url_for('owner_pup'))
    return render_template('pup_owner.html', form = oform)

@app.route('/toys', methods=['GET', 'POST'])
def toys_pup():
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
            flash("Toys %s for Puppy %s - Successfully added!" % (puppy.list_toys(), pup_name))
        return redirect(url_for('toys_pup'))
    return render_template('pup_toys.html', form = tform)

@app.route('/list')
def list_pup():
    with Session(engine) as session:  
        puppies = session.query(Puppy).all()
        return render_template('pup_list.html', puppies=puppies)

@app.route('/delete', methods=['GET', 'POST'])
def del_pup():
    dform = DelForm()
    if dform.validate_on_submit():
        id = dform.id.data
        with Session(engine) as session:
            rm_pup = session.query(Puppy).filter_by(id=id).one_or_none()
            session.delete(rm_pup)
            session.commit()
        flash("Puppy with ID %s - Successfully deleted!!" % id)
        return redirect(url_for('del_pup'))
    return render_template('pup_del.html', form = dform)


if __name__ == '__main__':
    app.run(debug=True)
