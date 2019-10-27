

import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://{user}:{passwd}@{host}:{port}/'\
    .format(user=os.environ.get("DB_USERNAME"),
            passwd=os.environ.get("DB_PASSWORD_MIYA"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"))

database_name = os.environ.get("DB_NAME")

print(database_name)
SECRET_KEY = "#d#JCqTTW\nilK\\7m\x0bp#\tj~#H"

STORE_APP_ID = 1116503637284883

DATABASE_URI = postgres_local_base+database_name
