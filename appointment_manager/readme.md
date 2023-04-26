
Readme

1 To run the app flawlessly, satisfy the requirements by installing the requirements.txt through terminal by giving command. 
	$ pip install -r requirements.txt

2. Please run all the servers in a linux based environment in windows use wsl.

3. Boot the servers for flask, celery-worker, celery-beat & redis by opening four terminals and type the following commands.
	a> python3 main.py
	b> celery -A main.celery worker -l info
	c> celery -A main.celery beat --max-interval 60 -l info
	d> redis-server

4. Please run the main.py file which is placed in the ProjectFolder, ProjectFolder is placed in the root directory of the zip file.

5. After running the app.py file in a terminal it will provide the default url which will be http://127.0.0.1:5000 .

6. The app will run on http://127.0.0.1:5000 , put this url on a browser and it will redirect you to the starting page of the app.

7. If you have an account login and if you don't have an account sign up.

8. The username and email is unique that is only one one account could be registered for one email and username.

9. After Signing up go to login page.

10. Provide the credentials for login i.e username and password.

11. After that it will redirect you to the user's dashboard.











