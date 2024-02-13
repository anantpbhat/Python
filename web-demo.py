
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')     ###127.0.0.1:5000/
def index():
    return "<h1>Hello World! Try puppy_latin page OR render a template!!</h1>"

@app.route('/info')     ###127.0.0.1:5000/info
def info():
    return "<h1>Website informational page.</h1>"

@app.route('/puppy_latin/<pupname>')
def puppylatin(pupname):
    if pupname.endswith('y'):
        latinpup = pupname.rstrip('y') + 'iful'
    else:
        latinpup = str(pupname) + 'y'
    return f"<h1>Latin name for {pupname} is {latinpup}</h1>"

@app.route('/testform')
def testform():
    return render_template('testhtml.html')


if __name__ == "__main__":
    app.run()
