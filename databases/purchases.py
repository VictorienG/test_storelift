from sqlalchemy import and_

from databases.models import Product, Buying


def find_id_product(s, name_product):
    """
    Return the id and the unit_price of the detected product.

    :param str name_product: Name of the detected product
    :param str brand: Brand of the detected product
    :return: The id of the detected product
    :rtype: tuple
    """
    id_product = s.query(Product).with_entities(Product.id_product, Product.unit_price).filter(
        Product.name.ilike(name_product)
    ).all()
    s.close

    return id_product[0]


def new_buying(s, id_store, id_customer, id_product, name_product, unit_price):
    """
    Associate a product with a customer if he has never taken the product since he entered the store.

    :param int id_store: The id of the store where the customer is entered
    :param int id_customer: The id of the customer.
    :param int id_product: The id of the detected product. The output of the find_id_product function.
    :param float unit_price: The unit price of the detected product. The output of the find_id_product function.
    :return: None
    """
    customer_buy_product = Buying(id_store=id_store, id_customer=id_customer, id_prod=id_product,
                                  name_product=name_product, quantity=1, unit_price=unit_price)
    s.add(customer_buy_product)
    s.commit()
    s.close()


def same_buying(s, id_store, id_customer, id_product):
    """
    Increase quantity of 1 for the product detected for the specified client.

    :param int id_store: The id of the store where the customer is entered
    :param int id_customer: The id of the customer.
    :param int id_product: The id of the detected product. The output of the find_id_product function.
    :return: None
    """
    change_quantity_product = s.query(Buying).filter(
        and_(
            Buying.id_store == id_store,
            Buying.id_customer == id_customer,
            Buying.id_prod == id_product
        )
    ).first()
    change_quantity_product.quantity = change_quantity_product.quantity + 1
    s.commit()
    s.close()


def put_product_in_store(s, id_store, id_customer, id_product):
    """
    Decrease quantity of 1 for the product detected for the specified client.

    :param int id_store: The id of the store where the customer is entered
    :param int id_customer: The id of the customer.
    :param int id_product: The id of the detected product. The output of the find_id_product function.
    :return: None
    """
    change_quantity_product = s.query(Buying).filter(
        and_(
            Buying.id_store == id_store,
            Buying.id_customer == id_customer,
            Buying.id_prod == id_product
        )
    ).first()
    change_quantity_product.quantity = change_quantity_product.quantity - 1
    s.commit()
    s.close()


def take_product(s, id_store, id_customer, name_product):
    """
    Orchestrates all actions when a customer takes a product.

    :param int id_store: The id of the store where the customer is entered
    :param int id_customer: The id of the customer.
    :param str name_product: Name of the detected product
    :param str brand: Brand of the detected product
    :return: None
    """
    (id_product, unit_price) = find_id_product(s, name_product)
    try:
        same_buying(s, id_store, id_customer, id_product)
    except:
        new_buying(s, id_store, id_customer, id_product, name_product, unit_price)


def return_product(s, id_store, id_customer, name_product):
    """
        Orchestrates all actions when a customer returns a product.

        :param int id_store: The id of the store where the customer is entered
        :param int id_customer: The id of the customer.
        :param str name_product: Name of the detected product
        :param str brand: Brand of the detected product
        :return:
    """
    (id_product, _) = find_id_product(s, name_product)
    put_product_in_store(s, id_store, id_customer, id_product)
