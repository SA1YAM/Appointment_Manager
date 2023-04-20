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


#from flask_security import Security, SQLAlchemyUserDatastore
#from application.data.models import db, User, Role
from flask_login import login_user, LoginManager, login_required, UserMixin, logout_user, current_user 



#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
login_manager = LoginManager()
#sec = Security()
