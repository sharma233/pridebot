# pridebot

## Setup

Create a virtual environment (Optional)

`python -m venv . --copies && source bin/activate`

Install the requirements

`pip install -r requirements.txt`

Install the dev requirements

`pip install -r dev-requirements.txt`

Create environment variables to store the DB connection information

`export DB_NAME="<db_name>"` (default: pride_db)

`export DB_HOST="<host>"` (default: localhost)

`export DB_PORT="<port>"` (default: 5432)

`export DB_USERNAME="<db_name>"` (default: postgres)

`export DB_PASSWORD="<db_name>"` (default: password)

`export BEARER_TOKEN="<bearer_token>"` (contact sharma233 or tromsky if you need a token)

Run the migrations

`python manage.py migrate` or `django-admin migrate` (equivalent commands)

## Running the server

To start a Django-aware shell, run

`python manage.py shell` or `django-admin shell` (equivalent commands)

To start the development server (default is http://127.0.0.1:8000/), run

`python manage.py runserver` or `django-admin runserver` (equivalent commands)

## Run the scrapper bot

Start a shell

`python manage.py shell`

Import the util functions

`from twitterbot.utils import *`

Run the scrape

`scrape_profile_pics()`
