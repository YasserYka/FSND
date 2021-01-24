
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Car(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)

    color = Column(String(80))

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    release =  Column(String(4), nullable=False)

    def json(self):

        return {
            'id': self.id,
            'color': self.color,
            'release': self.release
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Person(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)

    name = Column(String(80), unique=True)

    cars = db.relationship("Car", backref=db.backref('person', lazy=True))

    age =  Column(Integer(), nullable=False)

    def json(self):

        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()