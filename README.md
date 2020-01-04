# PugUghAPI

PugUghAPI is a demonstration of Django's API framework (Django Rest Framework) in the form of a dog profile app. A pre-built React frontend was provided and the objective was to build a 
backend with models, endpoints, serailizers, and views that handled each unique request. Additionally, all endpoints were protected by the requirement of a signed web token. 


<br/>

# installation

1. cd into your directory of projects (or wherever you prefer to keep your clones)
2. git clone ```https://github.com/Marksparkyryan/PugUghAPI.git``` to clone the app
3. ```virtualenv .venv``` to create your virtual environment
4. ```source .venv/bin/activate``` to activate the virtual environment
5. ```pip install -r PugUghAPI/requirements.txt``` to install app requirements
6. Run ```PugUghAPI/backend/pugorugh/scripts/data_import.py``` to populate the database with the provided json file
7. ```python manage.py runserver``` to serve the app to your local host
8. visit ```http://127.0.0.1:8000/``` to see the dogs (you'll have to register as a new user)! 


<br/>


# credits

Treehouse Techdegree Project 11
