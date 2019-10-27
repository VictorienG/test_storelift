from datetime import datetime

from databases.crud import s, pipeline_create_databases
from databases.entrance import entrance
from databases.exit import leave_the_store
from databases.get_data_for_api import get_purchases_names_from_customer
from databases.purchases import take_product, return_product
from store_app import app

if __name__ == "__main__":
    pipeline_create_databases()
    app.run(debug=True)
    s.close()
