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

from flask import render_template, url_for, redirect, request
from main import app, login_manager, bcrypt
from datetime import datetime
from flask_login import login_user, login_required, current_user, logout_user
from application.data.models import db, User, Appointment

# defining the login view 
login_manager.login_view = 'login'

# defining the user loader to return the appropriate user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

# root endpoint which return the login template   
@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("login.html")
        
        
# login endpoint which validates and logs in the user
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        
    if request.method == "POST":
        user_email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email = user_email).first()
        
        if user :
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                if current_user.is_authenticated:
                    return redirect(url_for('dashboard'))

            else:
                message = "Authentication Failed. The password is incorrect, Please try again and provide the correct password"
                return render_template("error.html", error_message = message, link = 'login')

        else:
            message = "Authentication Failed. User does not exists, Please verify the username and try again, If you don't have an account Sign Up"
            return render_template("error.html", error_message = message, link = 'login')
        
        
# register endpoint which return the register template  
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("Register.html")
              
        
# dashboard endpoint which returns the template binded with js files        
@app.route("/dashboard", methods= ["GET", "POST"])
@login_required
def dashboard():
    if current_user.is_authenticated:
        return render_template("Home.html")
        
        
        
        
# logout endpoint which logs out the user        
@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))