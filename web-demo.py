
from flask import Flask

app = Flask(__name__)

@app.route('/')     ###127.0.0.1:5000/
def index():
    return "<h1>Hello World!</h1>"

@app.route('/info')     ###127.0.0.1:5000/info
def info():
    return "<h1>Website informational page.</h1>"

@app.route('/person/<fullname>')
def person(fullname):
    return "<h2>Page for %s</h2>" % fullname.upper()


if __name__ == "__main__":
    app.run()
