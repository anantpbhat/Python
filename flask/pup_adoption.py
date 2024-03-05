from flask import Flask, render_template, url_for, redirect, flash
from pup_forms import AddForm, DelForm, OwnerForm, ToyForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pup_data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

class Puppy(db.Model):

    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref='puppy', uselist=False)
    toys = db.relationship('Toy', backref='puppy', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def list_owner(self):
        if self.owner:
            return self.owner.name
        else:
            return "None"

    def list_toys(self):
        if self.toys:
            for Ty in self.toys:
                return Ty.item_name.replace(',', ';')
        else:
            return "None"

    def __repr__(self):
        return f"Puppy name: {self.name}, Puppy ID: {self.id}, Puppy Owner: {self.list_owner()}, Puppy Toys: {self.list_toys()}"

class Owner(db.Model):

    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id

class Toy(db.Model):

    __tablename__ = 'toys'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, item_name, puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id

@app.route('/')
def index():
    return render_template('pup_home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    aform = AddForm()
    if aform.validate_on_submit():
        name = aform.name.data
        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()
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
        db.session.add(pup_owner)
        db.session.commit()
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
        db.session.add(pup_toys)
        db.session.commit()
        pup_name = pup_toys.puppy.name
        puppy = Puppy(pup_name)
        flash("Toys %s for Puppy %s - Successfully added!" % (puppy.list_toys(), pup_name))
        return redirect(url_for('toys_pup'))
    return render_template('pup_toys.html', form = tform)

@app.route('/list')
def list_pup():
    puppies = Puppy.query.all()
    return render_template('pup_list.html', puppies=puppies)

@app.route('/delete', methods=['GET', 'POST'])
def del_pup():
    dform = DelForm()
    if dform.validate_on_submit():
        id = dform.id.data
        rm_pup = Puppy.query.get(id)
        db.session.delete(rm_pup)
        db.session.commit()
        flash("Puppy with ID %s - Successfully deleted!!" % id)
        return redirect(url_for('del_pup'))
    return render_template('pup_del.html', form = dform)


if __name__ == '__main__':
    app.run(debug=True)
