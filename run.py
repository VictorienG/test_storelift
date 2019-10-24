from databases import crud
from databases.course import take_product, return_product
from databases.entrance import entrance
from databases.exit import leave_the_store

if __name__ == "__main__":
    # app.run(debug=True)
    crud.pipeline_create_databases()
    id_store_1 = 1
    id_store_2 = 2

    id_customer_1 = entrance(id_store_2, "Gimenez", "Victorien")
    id_customer_2 = entrance(id_store_1, "Pierre", "QuiRoule")

    take_product(id_store_2, id_customer_1, "evian 1l", "evian")
    take_product(id_store_2, id_customer_1, "evian 1l", "evian")
    take_product(id_store_2, id_customer_1, "evian 1l", "evian")
    take_product(id_store_2, id_customer_1, "KitKat paquet de 6", "Nestle")
    return_product(id_store_2, id_customer_1, "evian 1l", "evian")

    leave_the_store(id_store_2, id_customer_1)
