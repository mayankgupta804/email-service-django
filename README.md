# A Django Web Application which acts an email portal service for admins

### How to start the project

* Create a new virtual environment using *vitualenv -p python3 venv*.
* Activate it using *source venv/bin/activate*. 
* Install the dependencies using *pip install requirements.txt*.
* Make the migrations using *python manage.py migrate*
* Run the server using *python manage.py runserver*.
* Run the celery worker using *celery -A email_service worker -l info* in another terminal with your virtual environment activated. Make sure you have set the RabbitMQ URL in your environment.
* Run celery beat using *celery -A email_service beat -l info* in another terminal, again with your virtual environment actvated.
* Go to *http://localhost:8000*, write an email and check your *celery worker* terminal. You should see that it sends the mail and prints the contents in the console.
* Go to the terminal where your *celery beat* process is running and you would see that every 30 minutes it prints to the console the email stats for the day.