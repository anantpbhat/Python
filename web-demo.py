import re

from flask import Flask
import re

app = Flask(__name__)

@app.route('/')     ###127.0.0.1:5000/
def index():
    return "<h1>Hello World! Try 'puppy_latin' page!!</h1>"

@app.route('/info')     ###127.0.0.1:5000/info
def info():
    return "<h1>Website informational page.</h1>"

@app.route('/person/<fullname>')
def person(fullname):
    return "<h2>Page for %s</h2>" % fullname.upper()

@app.route('/puppy_latin/<pupname>')
def puppylatin(pupname):
    if pupname.endswith('y'):
        latinpup = pupname.rstrip('y') + 'iful'
    else:
        latinpup = str(pupname) + 'y'
    return f"<h1>Latin name for {pupname} is {latinpup}</h1>"


if __name__ == "__main__":
    app.run()
