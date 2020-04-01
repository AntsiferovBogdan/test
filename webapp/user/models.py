from flask_login import UserMixin
from webapp.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(48))
    name = db.Column(db.String(24))
    middle_name = db.Column(db.String(48))
    incident_counter = db.Column(db.Integer)
    crime_status = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.surname} {self.name} {self.middle_name}; \n Количество инцидентов - {self.incident_counter}'
