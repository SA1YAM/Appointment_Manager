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


from main import celery, mail, app
from flask_mail import Message
from flask import render_template, url_for
from application.data.models import db, User, Appointment
from datetime import datetime, timedelta
import csv
import io
from celery.schedules import crontab


# generates the csv file for the appointments 
def generate_csv(appointments):
#    field_names= ["Post_Id", "Title", "caption", "Timestamp", "Image_Url", "Archive_Switch", "Total_Likes", "Total_Comments"]
    field_names= ["appointment_id", "Title", "Client", "Scheduled Time", "Remarks"]
    data = []
    for appt in appointments:
#        print(len(post.likes))
#        row = {"Post_Id": post.post_id, "Title": post.title, "caption": post.caption, "Timestamp": post.time_stamp.strftime('%d/%m/%Y %H:%M'), "Image_Url": post.image_url, "Archive_Switch": post.archive_switch , "Total_Likes": len(post.likes), "Total_Comments": len(post.comments) }
        row = {"appointment_id": appt.appointment_id, "Title": appt.title, "Client": appt.client, "Scheduled Time": appt.scheduled_time.strftime('%d/%m/%Y %H:%M'), "Remarks": appt.remarks}
        data.append(row)
        
    file_output = io.StringIO()
    
    
    writer = csv.DictWriter(file_output, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)
        
    file_output.seek(0)
    return file_output
        
    
# send the csv file to the user via mail
@celery.task
def export_csv(user_id):

    current_user = User.query.get(user_id)
    
    csv_file = generate_csv(current_user.appointments)
    
    msg = Message(recipients=[current_user.email],
                  body = "Hey " + current_user.username +  ", Please find your attached csv file.",
                  subject = "Exported csv file")
                  
    msg.attach("appointments.csv", "text/csv", csv_file.read())
    
    mail.send(msg)
#    print("sent")
    
    
#setting up the peroidic tasks
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Executes in every 15 minutes.
    sender.add_periodic_task(
        crontab(minute='*/15'),
        delete_appointments.s(),
        name = "delete expired appointments"
    )


    
 
# defining the delete operation which is executed periodically to delete the expired appointments
@celery.task 
def delete_appointments():
    users = User.query.all()
    
    current_time = datetime.now()
    
    for user in users:
        for appt in user.appointments:
            if appt.scheduled_time < current_time:
                delayed_appointment = Appointment.query.get(appt.appointment_id)
                db.session.delete(delayed_appointment)
                db.session.commit()
                        
            
                
                
         
         
         