from databases.crud import s
from databases.models import Store, Stock, Buying


def get_stores():
    stores = s.query(Store).with_entities(Store.name_store, Store.id_store).all()
    return stores


def get_products_from_store(id_store):
    products = s.query(Stock).with_entities(Stock.id_prod, Stock.name_product, Stock.quantity).filter(
        Stock.id_store == id_store,
        Stock.quantity > 0
    ).distinct().all()
    return products


def get_products_from_customer(id_store, id_customer):
    products = s.query(Buying).with_entities(Buying.id_prod, Buying.name_product, Buying.quantity).filter(
        Buying.id_store == id_store,
        Buying.id_customer == id_customer,
        Buying.quantity > 0
    ).distinct().all()
    return products
