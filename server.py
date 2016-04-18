#Aidan San
#muakasan@gmail.com
#https://github.com/Muakasan/

from flask import jsonify, Flask, render_template, request, send_from_directory, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
import os
from math import hypot
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'pdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/pdfdb'
db = SQLAlchemy(app)


novalatitude = 38.6219283
novalongitude = -77.2918893

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, name, password, link):
        self.name = name
        self.password = password

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf-input[]']
    if file:
        filename = secure_filename(file.filename)
        print("filename", filename)
        print("password:", request.form['password'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if not db.session.query(File).filter(File.name == filename).count():
            db.session.add(File(filename, request.form['password'], random.randint(0, 10000000)))
            db.session.commit()
            print("should have added")
        print("didnt add")

    return "okay"

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def downloads(filename):
    print(filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)

@app.route('/download', methods=['GET'])
def download():  
    return render_template("download.html")

@app.route('/downloadp', methods=['POST'])
def downloadp():  
    print("ayyyy")
    filename = request.json['filename'] 
    password = request.json['password']
    print(filename)
    print(password)
    if hypot(request.json['lat']-novalatitude, request.json['long']-novalongitude) < .1:
        someFiles = db.session.query(File).filter(File.name == filename and File.password == password)
        if someFiles:
            print("should have downloaded")
            return ("/uploads/" + filename)
    return "/uploaderror"

@app.route('/uploaderror', methods=['GET'])
def uploadError():
    return render_template("uploaderror.html")

if  __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
