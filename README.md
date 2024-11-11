foodTracker app
track your meals with this app 

First create and activate a virtual environment:
    python -m venv venv
    source venv\Scripts\activate
    pip install -r requirements.txt
Than create the database and superuser
    python manage.py migrate
    python manage.py createsuperuser

Now run the server
    python manage.py runserver

add foods that you like and log your meals


GitHub link : https://github.com/MichalHir/Food-Tracker-Django


