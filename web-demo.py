
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')     ###127.0.0.1:5000/
def index():
    return render_template('index.html')

@app.route('/puppy_latin/<pupname>')
def puppylatin(pupname):
    if pupname.endswith('y'):
        latinpup = pupname.rstrip('y') + 'iful'
    else:
        latinpup = str(pupname) + 'y'
    return f"<h1>Latin name for {pupname} is {latinpup}</h1>"

@app.route('/signup_form')
def signup_form():
    return render_template('signup.html')

@app.route('/thank_you')     ###127.0.0.1:5000/info
def thank_you():
    first = request.args.get('first')
    last = request.args.get('last')
    return render_template('thankyou.html', first=first, last=last)

@app.errorhandler(404)
def url_error(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()
