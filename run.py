from datetime import datetime

from databases import crud
from databases.crud import s
from databases.entrance import entrance
from databases.exit import leave_the_store
from databases.get_data_for_api import get_name_product_from_id, get_purchases_id_from_customer, \
    get_purchases_names_from_customer
from databases.purchases import take_product, return_product
from store_app import app

if __name__ == "__main__":
    crud.pipeline_create_databases()
    app.run(debug=True)

    """ id_store_1 = 1
    id_store_2 = 2

    id_customer_1 = entrance(id_store_2, "Gimenez", "Victorien")
    id_customer_2 = entrance(id_store_1, "Pierre", "QuiRoule")

    take_product(id_store_2, id_customer_1, "evian 1l")
    take_product(id_store_2, id_customer_1, "evian 1l")
    take_product(id_store_2, id_customer_1, "evian 1l")
    take_product(id_store_2, id_customer_1, "KitKat paquet de 6")
    return_product(id_store_2, id_customer_1, "evian 1l")

    leave_the_store(id_store_2, id_customer_1)
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M")
    get_purchases_names_from_customer(id_customer_1, id_store_2, now)"""
    s.close()
