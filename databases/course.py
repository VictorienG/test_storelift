from sqlalchemy import and_

from databases.crud import s
from databases.models import Product, Buying


def find_id_product(name_product, brand):
    """
    Return the id and the unit_price of the detected product.

    :param String name_product: Name of the detected product
    :param String brand: Brand of the detected product
    :return: The id of the detected product
    :rtype: Tuple
    """
    id_product = s.query(Product).with_entities(Product.id_product, Product.unit_price).filter(
        and_(
            Product.name.ilike(name_product),
            Product.brand.ilike(brand)
        )
    ).all()
    s.close
    return id_product[0]


def new_buying(id_store, id_customer, id_product, unit_price):
    """
    Associate a product with a customer if he has never taken the product since he entered the store.

    :param Integer id_store: The id of the store where the customer is entered
    :param Integer id_customer: The id of the customer.
    :param Integer id_product: The id of the detected product. The output of the find_id_product function.
    :param Float unit_price: The unit price of the detected product. The output of the find_id_product function.
    :return: None
    """
    customer_buy_product = Buying(id_store=id_store, id_customer=id_customer, id_prod=id_product, quantity=1,
                                  unit_price=unit_price)
    s.add(customer_buy_product)
    s.commit()
    s.close()


def same_buying(id_store, id_customer, id_product):
    """
    Increase quantity of 1 for the product detected for the specified client.

    :param Integer id_store: The id of the store where the customer is entered
    :param Integer id_customer: The id of the customer.
    :param Integer id_product: The id of the detected product. The output of the find_id_product function.
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


def take_product(id_store, id_customer, name_product, brand):
    """
    Orchestrates all actions when a customer takes a product.

    :param Integer id_store: The id of the store where the customer is entered
    :param Integer id_customer: The id of the customer.
    :param String name_product: Name of the detected product
    :param String brand: Brand of the detected product
    :return: None
    """
    (id_product, unit_price) = find_id_product(name_product, brand)
    try:
        same_buying(id_store, id_customer, id_product)
    except:
        new_buying(id_store, id_customer, id_product, unit_price)
    pass


def return_product(id_store, id_customer, name_product, brand):
    """
        Orchestrates all actions when a customer returns a product.

        :param Integer id_store: The id of the store where the customer is entered
        :param Integer id_customer: The id of the customer.
        :param String name_product: Name of the detected product
        :param String brand: Brand of the detected product
        :return:
    """
    (id_product, unit_price) = find_id_product(name_product, brand)
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
    pass
