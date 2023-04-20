import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
#print(current)

parentt = os.path.dirname(current)
sys.path.append(parentt)
#print("parentt",parentt)

parent = os.path.dirname(parentt)
sys.path.append(parent)
#print("parent",parent)
 

from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields, request
from flask import jsonify, render_template, url_for, redirect, request
from application.data.models import db, User, Appointment
from application.jobs.tasks import export_csv
#from application.config import store_img
from main import app, cache, bcrypt, login_manager
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from flask_login import login_user, login_required, current_user, logout_user

# instantiating the api object and binding it with our app
api = Api(app)
    
#input arguements for user        
args_user = reqparse.RequestParser()
args_user.add_argument('username', type = str, required = True)
args_user.add_argument('Password', type = str, required = True)
args_user.add_argument('full_name', type = str, required = True)
args_user.add_argument('email', type = str, required = True)
args_user.add_argument('dob', type = str, required = True)
    
  
#input arguements for changing password
args_changePass = reqparse.RequestParser()
args_changePass.add_argument('email', type = str, required = True)
args_changePass.add_argument('oldPassword', type = str, required = True)
args_changePass.add_argument('newPassword', type = str, required = True)

  
#formatting of date        
class ChangeDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%d/%m/%Y %H:%M')
        

#output fields of user        
user_fields = {
    "id" : fields.Integer,
    "username" : fields.String,
    "email" : fields.String,
    "dob": ChangeDateFormat,
    "errors": fields.List(fields.String),
}


# check the validity of email
def check_email(email):

    try:
      # validate and get info
        validation = validate_email(email, check_deliverability = True)
        # replace with normalized form
#        print(validation.email)
        validity = True
        
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
#        print(str(e))
        validity = False
        
    return validity


#user api class for CRUD operations
class Users(Resource):

    @marshal_with(user_fields)
    def post(self):
        args = args_user.parse_args()
        
        
        errors_list = []
        
        if args["username"]:
            user_name = User.query.filter_by(username = args["username"]).first()
            if user_name:
                errors_list.append("username already exists please choose a diffrent one")
                    
            if len(args["username"]) > 30:
                errors_list.append("username should be less than 20 characters")  
                
            if " " in args["username"] :
                errors_list.append("username should not contain any spaces") 
               
               
        else:
            errors_list.append("username can not be empty")
            
            
        if args["email"]:
            user_email = User.query.filter_by(email = args["email"]).first()
            if user_email:
                errors_list.append("email already exists please choose a diffrent one")
                
            if not check_email(args["email"]):
                errors_list.append("Please choose a valid email")
                
        else:
            errors_list.append("email can not be empty")
              
            
        if args["dob"]:
            if datetime.strptime(args["dob"], '%Y-%m-%d') < datetime.now():
                sssdob = 5
#                print(args["dob"])
                 
            else:
                errors_list.append("please choose a valid dob") 
                
        else:
            errors_list.append("Date of birth can not be empty")
            
            
        if args["full_name"]:
            if len(args["full_name"]) > 40:
                errors_list.append("full name should be less than 50 characters") 
            
            if len(args["full_name"].strip()) == 0:
                errors_list.append("Full Name cannot contain only whitespaces")
                
        else:
            errors_list.append("full name can not be empty")
            
        if args["Password"]:
            if len(args["Password"]) < 5:
                errors_list.append("password should contain atleast 5 characters") 
                
            if " " in args["Password"] :
                errors_list.append("password should not contain any spaces") 
                
        else:
            errors_list.append("password can not be empty")
            
        if len(errors_list) > 0:
#            print(errors_list)
            error = {}
            error["errors"] = errors_list
            
            return error, 409

        
        new_user = User(
            username = args["username"],
            password = bcrypt.generate_password_hash(args["Password"]),
            full_name = args["full_name"],
            email = args["email"],
            created_at = datetime.now(),
            dob = datetime.strptime(args["dob"], '%Y-%m-%d'),
        )
        
        db.session.add(new_user)
        db.session.commit()
        
#        print(user)
            
        cache.clear()
                
        return new_user, 201
        
      
    
    @login_required
    def delete(self):
        if current_user.is_authenticated:
    
            args = args_user.parse_args()
            
            errors_list = []
            
            if args["username"] != current_user.username:
                errors_list.append("username does not match")
                
            if args["email"] != current_user.email:
                errors_list.append("email does not match")    
            
            if args["full_name"] != current_user.full_name:
                errors_list.append("Full name does not match") 
                
            if args["Password"]:
                if not bcrypt.check_password_hash(current_user.password, args["Password"]):
                    errors_list.append("Password does not match") 
                    
            else:
                errors_list.append("password can not be empty")
            
            if args["dob"]:
                if datetime.strptime(args["dob"], '%Y-%m-%d') != current_user.dob:
                    errors_list.append("Date of birth does not match")   
            else:
                errors_list.append("Date of birth does not match") 
                
            if len(errors_list) > 0:
#                print(errors_list)
                error = {}
                error["errors"] = errors_list
                
                return error, 409
                
            cache.clear()
            
            
            user = User.query.get(current_user.id)
            db.session.delete(user)
            db.session.commit()
#            print("deleted")
            return 200
            
            
            
    @login_required
    def put(self):
        if current_user.is_authenticated:
    
            args = args_changePass.parse_args()
            
            errors_list = []
            
            if args["email"]:
                if args["email"] != current_user.email:
                    errors_list.append("email does not match") 
                    
            else:
                errors_list.append("Email can not be empty")

            user = User.query.get(current_user.id)
            
            if args["oldPassword"]:
                if not bcrypt.check_password_hash(user.password, args["oldPassword"]):
                    errors_list.append("Current Password does not match") 
                    
            else:
                errors_list.append("Current password can not be empty")

            if args["newPassword"]:
                if len(args["newPassword"]) < 5:
                    errors_list.append("password should contain atleast 5 characters") 
                    
                if " " in args["newPassword"] :
                    errors_list.append("password should not contain any spaces") 
                    
            else:
                errors_list.append("New password can not be empty")
                
            if len(errors_list) > 0:
#                print(errors_list)
                error = {}
                error["errors"] = errors_list
                
                return error, 409
                
            cache.clear()
            
            
            user.password = bcrypt.generate_password_hash(args["newPassword"])
            db.session.commit()
#            print("deleted")
            return 200
        
        
        
    @login_required
    @cache.cached(timeout=10)
    @marshal_with(user_fields)
    def get(self):
        if current_user.is_authenticated:
            return current_user, 200
               
api.add_resource(Users, "/api/user")
        

#output fields of appointment
appointment_fields = {
    "appointment_id" : fields.Integer,
    "title": fields.String,
    "client" : fields.String,
    "remarks" : fields.String,
    "scheduled_time" : ChangeDateFormat,
    "user_id" : fields.Integer,
    "errors": fields.List(fields.String),
}

            
# output field of user containing the list of all created appointments        
user_fields1 = {
    "id" : fields.Integer,
    "username" : fields.String,
    "appointments": fields.List(fields.Nested(appointment_fields)),
    "total_appointments": fields.Integer,
}



# first view of the dashboard of application viewed after login
class MyProfile(Resource):

    @login_required
    @cache.cached(timeout=10)
    @marshal_with(user_fields1)
    def get(self):
        if current_user.is_authenticated:
        
            user = {}
            user["id"] = current_user.id
            user["username"] = current_user.username
            user["appointments"] = sorted(current_user.appointments, key = lambda appointment: appointment.scheduled_time) 
            user["total_appointments"] = len(current_user.appointments)
            
            return user, 200
                
api.add_resource(MyProfile, '/api/myprofile')
        

# input arguements for appointment
args_appt = reqparse.RequestParser()
args_appt.add_argument('title', type = str, required = True)
args_appt.add_argument('client', type = str, required = True)
args_appt.add_argument('remarks', type = str, required = True)
args_appt.add_argument('date', type = str, required = True)
args_appt.add_argument('time', type = str, required = True)



#appointments api class for CRUD operations
class Appointments(Resource):

    @login_required
    @cache.memoize(timeout=10)
    @marshal_with(appointment_fields)
    def get(self, appointment_id):
        if current_user.is_authenticated:
            appt = Appointment.query.get(appointment_id)
            
#            print(post)
            return appt, 200
   
   
                
                
    @login_required
    @marshal_with(appointment_fields)
    def post(self):
    
        if current_user.is_authenticated:
            
            args = args_appt.parse_args()
                
            errors_list = []
            cache.clear()
            
            schedule_time = args["date"] + " " + args["time"]
            
            sch_date = datetime.strptime(schedule_time, '%Y-%m-%d %H:%M')
            
            if sch_date > datetime.now():
                sssdob = 5
#                print(args["dob"])
                 
            else:
                errors_list.append("please choose a valid date") 
                
            if len(errors_list) > 0:
#            print(errors_list)
                error = {}
                error["errors"] = errors_list
            
                return error, 409
            
            appntmnt = Appointment(title = args["title"], client = args["client"], remarks = args["remarks"], scheduled_time = sch_date, user_id = current_user.id)
            db.session.add(appntmnt)
            db.session.commit()
            return appntmnt,  201
                                
                
                
    @login_required
    @marshal_with(appointment_fields)
    def put(self, appointment_id):
    
        if current_user.is_authenticated:
        
            args = args_appt.parse_args()
                
            errors_list = []
            cache.clear()
            
            schedule_time = args["date"] + " " + args["time"]
            
            sch_date = datetime.strptime(schedule_time, '%Y-%m-%d %H:%M')
            
            if sch_date > datetime.now():
                sssdob = 5
#                print(args["dob"])
                 
            else:
                errors_list.append("please choose a valid date") 
                
            if len(errors_list) > 0:
#            print(errors_list)
                error = {}
                error["errors"] = errors_list
            
                return error, 409
            
                
            appt = Appointment.query.get(appointment_id)
            appt.title = args["title"]
            appt.client = args["client"]
            appt.remarks = args["remarks"]
            appt.scheduled_time = sch_date
                
            db.session.commit()
                
            return appt,  200

            
            
                            
                
    
    @login_required
    def delete(self, appointment_id):
        if current_user.is_authenticated:
            appt = Appointment.query.get(appointment_id)
            db.session.delete(appt)
            db.session.commit()
            
            cache.clear()
            
            
            return 200 

api.add_resource(Appointments, "/api/appointment", "/api/appointment/<int:appointment_id>")


# search api class for searching the appointments
class Search(Resource):

    @login_required
    @cache.cached(timeout = 10)
    @marshal_with(appointment_fields)
    def get(self):
        if current_user.is_authenticated:
#            value = request.args.get("value")
#            print(value)
            
            appt_list = current_user.appointments

            
#            print(users)
            return appt_list, 200
          
api.add_resource(Search, '/api/search')



            
# output message for export
export_fields = {
    "message": fields.String,
}


# export api class for exporting the appointments    
class Exportcsv(Resource):

    @login_required
    @cache.cached(timeout = 10)
    @marshal_with(export_fields)
    def get(self):
        if current_user.is_authenticated:
            
            res = export_csv.delay(current_user.id)
#            print(res, res.ready())
            
            
            return {"message": "Export request sent. a csv file will be mailed to your email"}, 200
            
            
                        
api.add_resource(Exportcsv, '/api/export')
            