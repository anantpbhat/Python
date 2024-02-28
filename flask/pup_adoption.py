from flask import Flask, render_template, url_for, redirect
from pup_forms import AddForm, DelForm
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

    def list_toys(self):
        Toys = []
        if self.toys:
            for Ty in self.toys:
                Toys.append(Ty.item_name)
            toy_list = ','.join(Toys)
        return toy_list

    def __repr__(self):
        if self.owner.name and len(self.list_toys()) > 0:
            return f"Puppy name: {self.name}, Puppy ID: {self.id}, Puppy Owner: {self.owner.name}, Puppy Toys: {self.list_toys()}"
        elif self.owner.name and len(self.list_toys()) == 0:
            return f"Puppy name: {self.name}, Puppy ID: {self.id}, Puppy Owner: {self.owner.name}, Puppy Toys: None"
        elif len(self.list_toys()) > 0 and not self.owner.name:
            return f"Puppy name: {self.name}, Puppy ID: {self.id}, Puppy Toys: {self.list_toys()}, Puppy Owner: None"
        else:
            return f"Puppy name: {self.name}, Puppy ID: {self.id}, Puppy Owner: None, Puppy Toys: None"

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
        owner = aform.owner.data
        toys = aform.toys.data
        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()
        pup = Puppy.query.filter_by(name=name).first()
        pup_owner = Owner(owner, pup.id)
        pup_toys = Toy(toys, pup.id)
        db.session.add_all([pup_owner, pup_toys])
        db.session.commit()
        return redirect(url_for('list_pup'))
    return render_template('pup_add.html', form = aform)

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
        return redirect(url_for('list_pup'))
    return render_template('pup_del.html', form = dform)


if __name__ == '__main__':
    app.run(debug=True)
