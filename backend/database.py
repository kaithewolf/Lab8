from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lab8.sqlite" 
db = SQLAlchemy(app)

class User(db.Model):
    u_name = db.Column(db.String, primary_key=True)
    u_password = db.Column(db.String, nullable=False)
    u_type = db.Column(db.String, nullable=False)

class Classes(db.Model):
    c_classkey = db.Column(db.Integer, nullable=False, primary_key=True)
    c_classname = db.Column(db.String, nullable=False)
    c_teacher = db.Column(db.String, nullable=False)
    c_time = db.Column(db.String, nullable=False)
    c_seats = db.Column(db.Integer, nullable=False)

class Students_in_Classes(db.Model):
    sc_classkey = db.Column(db.Integer, nullable=False, primary_key=True)
    sc_name = db.Column(db.String, nullable=False)
    sc_grade = db.Column(db.Integer, nullable=False)

db.create_all()
    
