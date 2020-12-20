# Online Learn - Django App


#### Link for website: https://frasulov.pythonanywhere.com

## How to run Web app in your local host?

* Firstly download python and pip.
* Secondly download all requirements from requirement.txt file.
* Then come to mysite folder (where manage.py is located) and run following commands
	* python manage.py makemigrations
	* python manage.py migrate
	* python manage.py createsuperuser  # it will ask mail and password for creating user.
* Now, lets run our app by running following command
	* python manage.py runserver

##### You will see such text in the result.
Starting development server at http://127.0.0.1:8000/
##### Just open http://127.0.0.1:8000/ the url in your browser.