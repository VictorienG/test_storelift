# test_storelift
# test_storelift
This Repo is an example of an API for Storelift. The database used is Postgress and the demo is a flask application.

This is how the repo is ordered :

- Databases -> All functions that interact with the database are here
    - crud -> Create the database and fill it.
    - entrance -> Contain all functions for the customer's entrance
    - exit -> Contain all functions for the customer's exit
    - fill_dbs -> Create data used in crud to fill the database
    - get_data_for_api -> Contain all functions used to display data in the html
    - models -> Contain the schema of the database
    - purchases -> Contain all functions for the customer purchases

- store_app -> Contains all data and functions used in the front
    - static -> Contain the css file
    - templates -> Contain all html files
    - views -> The flask application that allows to interact with the front and the database

 - config -> Contain all constants
 - Dockerfile -> The dockerfile not test here
 - requirements -> The requirements
 - run -> The entry point of the project

Pour lancer le projet, il faut créer la base de données avant et modifichier le fichier config. Pas besoins de créer
les tables