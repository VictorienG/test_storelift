from databases.crud import s
from databases.models import Store, Stock, Buying, HistoryCustomer, Product


def get_stores():
    """
    Return all stores in the database.

    :return: All stores in the database
    :rtype: list
    """
    stores = s.query(Store).with_entities(Store.name_store, Store.id_store).all()
    s.close()
    return stores


def get_products_in_store(id_store):
    """
    Return all products for a store.
    The format is [(id_prod_1, name_prod_1, quantity_1), (id_prod_1, name_prod_1, quantity_1), ...]

    :param int id_store: The id of the store where are products
    :return: All product for a store
    :rtype: list
    """
    products = s.query(Stock).with_entities(Stock.id_prod, Stock.name_product, Stock.quantity).filter(
        Stock.id_store == id_store,
        Stock.quantity > 0,
    ).distinct().all()
    s.close()
    return products


def get_products_in_buying_for_customer(id_store, id_customer):
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
    s.close()
    return products


def get_quantity_for_product_customer_in_buying(id_store, id_customer, id_product):
    """
    The quantity of the product corresponding to the id_product.
    If the product does not exist in the Buying table, the function returns 0.

    :param int id_store: The id of the store
    :param int id_customer: The id of the customer
    :param int id_product: The id of the product
    :return: The quantity of the product corresponding to the id_product
    :rtype: int
    """
    quantity = s.query(Buying).with_entities(Buying.quantity).filter(
        Buying.id_store == id_store,
        Buying.id_customer == id_customer,
        Buying.id_prod == id_product
    ).first()
    s.close()
    if quantity is None:
        return 0
    else:
        return quantity[0]


def get_available_product_for_customer(id_store, id_customer):
    """
    Return all available products for the customer.
    A product is considered available if the customer has taken less product than there is in the storage.

    :param int id_store: The id of the store
    :param int id_customer: The id of the customer
    :return: The list of available products for the customer
    :rtype: list
    """
    available_product = []
    product_stock = get_products_in_store(id_store)
    for id_product, name_product, quantity_product_stock in product_stock:
        quantity_product_customer = get_quantity_for_product_customer_in_buying(id_store, id_customer, id_product)
        if quantity_product_stock > quantity_product_customer:
            available_product.append((id_product, name_product, quantity_product_stock))

    return available_product


def get_purchases_id_from_customer(id_customer, id_store, date_inf):
    """
    Return all purchases for a given customer and store. Return all products whom the customer buy after the date_inf.
    The format looks like : [(date_1, id_prod_1, quantity_1), (date_2, id_prod_2, quantity_2), ...]

    :param int id_customer: The id of the customer
    :param int id_store: The id of the store
    :param datetime date_inf: The date to filter the purchases
    :return: All purchases in HistoryCustomer table for the customer and the store
    :rtype: list
    """
    purchases = s.query(HistoryCustomer).with_entities(HistoryCustomer.date, HistoryCustomer.id_prod,
                                                       HistoryCustomer.quantity).filter(
        HistoryCustomer.id_customer == id_customer,
        HistoryCustomer.id_store == id_store,
        HistoryCustomer.date >= date_inf,
    ).all()
    s.close()
    return purchases


def get_name_product_from_id_product(id_product):
    """
    Return the name of the corresponding id product

    :param int id_product: The id of the product
    :return: The name of the product
    :rtype: str
    """
    name_product = s.query(Product).with_entities(Product.name).filter(
        Product.id_product == id_product
    ).first()
    s.close()
    return name_product[0]


def get_purchases_names_from_customer(id_customer, id_store, date_inf):
    """
    Return all purchases for a given customer and store. Return all products whom the customer buy after the date_inf.
    The format looks like : [(date_1, name_prod_1, quantity_1), (date_2, name_id_prod_2, quantity_2), ...]

    :param int id_customer: The id of the customer
    :param int id_store: The id of the store
    :param datetime date_inf: The date to filter the purchases
    :return: All purchases in HistoryCustomer table for the customer and the store
    :rtype: list
    """
    purchases = get_purchases_id_from_customer(id_customer, id_store, date_inf)
    purchase_with_product_name = []
    for date_purchase, id_product, quantity in purchases:
        name_product = get_name_product_from_id_product(id_product)
        purchase_with_product_name.append((date_purchase, name_product, quantity))
    return purchase_with_product_name
