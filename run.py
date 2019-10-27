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




    """id_store_1 = 1
    id_store_2 = 2

    id_customer_1 = entrance(s, id_store_2, "Gimenez", "Victorien")
    id_customer_2 = entrance(s, id_store_1, "Pierre", "QuiRoule")

    take_product(s, id_store_2, id_customer_1, "evian 1l")
    take_product(s, id_store_2, id_customer_1, "evian 1l")
    take_product(s, id_store_2, id_customer_1, "evian 1l")
    take_product(s, id_store_2, id_customer_1, "KitKat paquet de 6")
    return_product(s, id_store_2, id_customer_1, "evian 1l")

    leave_the_store(s, id_store_2, id_customer_1)
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M")
    get_purchases_names_from_customer(id_customer_1, id_store_2, now)"""
    s.close()
