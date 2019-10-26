from databases.crud import s
from databases.models import Store, Stock, Buying


def get_stores():
    """
    Return all stores in the database.

    :return: All stores in the database
    :rtype: list
    """
    stores = s.query(Store).with_entities(Store.name_store, Store.id_store).all()
    return stores


def get_products_from_store(id_store):
    """
    Return all products for a store.
    The format is [(id_prod_1, name_prod_1, quantity_1), (id_prod_1, name_prod_1, quantity_1), ...]

    :param int id_store: The id of the store where are products
    :return: All product for a store
    :rtype: list
    """
    products = s.query(Stock).with_entities(Stock.id_prod, Stock.name_product, Stock.quantity).filter(
        Stock.id_store == id_store,
        Stock.quantity > 0
    ).distinct().all()
    return products


def get_products_from_customer(id_store, id_customer):
    """
    Return all product for a store and a customer. It looks for the products in the Buying table.

    :param int id_store: The id of the store
    :param int id_customer: The id of the customer
    :return: All products that the customer wants to buy
    :rtype: list
    """
    products = s.query(Buying).with_entities(Buying.id_prod, Buying.name_product, Buying.quantity).filter(
        Buying.id_store == id_store,
        Buying.id_customer == id_customer,
        Buying.quantity > 0
    ).distinct().all()
    return products
