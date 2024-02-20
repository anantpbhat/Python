from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

class InfoForm(FlaskForm):
    breed = StringField('What Dog breed is your pet?')
    submit = SubmitField('Click Here')

@app.route('/', methods = ['GET', 'POST'])
def home():
    breed = False
    form = InfoForm()
    if form.validate_on_submit():
        session['breed'] = form.breed.data
        flash('Dog breed you specified was - %s' % session['breed'])
        form.breed.data = ''
        return redirect(url_for('home'))
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
