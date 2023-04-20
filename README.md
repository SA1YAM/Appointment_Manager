# Appointment_Manager
This is a web based application which is used for managing the appointments. Cookie based authentication is used for security. This app has to run on linux based environment because redis and celery have been used in the application.
I have also added the export option which can export all the appointments in a csv format. I have also added caching at the backend by binding redis with flask caching.
I have also used Celery in order to automate the tasks and to add asynchronus batch processing at my backend.
