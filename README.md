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