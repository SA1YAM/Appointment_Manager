import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
#print(current)

parentt = os.path.dirname(current)
#print(parentt)

parent = os.path.dirname(parentt)
#print(parent)

sys.path.append(parent)
sys.path.append(parentt)



from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin 

# instantiationg the SQLAlchemy object
db = SQLAlchemy() 
        
# defing the user model for database
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    full_name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(), unique = True, nullable = False)
    created_at = db.Column(db.DateTime(), nullable = False)
    dob = db.Column(db.DateTime(), nullable = False)
    appointments = db.relationship('Appointment', backref = 'user', cascade = "all, delete", lazy = True)
    
 #defining the appointment model for database   
class Appointment(db.Model):
    __tablename__ = 'appointment'
    appointment_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    title = db.Column(db.String(), nullable = False)
    client = db.Column(db.String(), nullable = False)
    remarks = db.Column(db.String(), nullable = False)
    scheduled_time = db.Column(db.DateTime(), nullable = False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)
