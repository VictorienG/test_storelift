from sqlalchemy import and_

from databases.crud import s
from databases.models import Stock, IsInStore, Buying, HistoryCustomer
from datetime import datetime


def change_stock(id_store, id_product, quantity_bought):
    """
    Change the stock of the store for a product and a given quantity.

    :param Integer id_store: The id of the store
    :param Integer id_product:  The id of the product
    :param Integer quantity_bought: The quantity to take off.
    :return: None
    """
    change_quantity_stock = s.query(Stock).filter(
        and_(
            Stock.id_store == id_store,
            Stock.id_prod == id_product
        )
    ).first()
    change_quantity_stock.quantity = change_quantity_stock.quantity - quantity_bought
    s.commit()
    s.close()


def compute_total_price(id_store, id_customer):
    """
    Compute the total price for a customer and return all products bought with their corresponding quantity.

    :param Integer id_store: The id of the store
    :param Integer id_customer: he id of the customer
    :return: The total price for the customer
    :rtype: Tuple
    """
    total_price = 0
    products_bought = []
    all_products = s.query(Buying).with_entities(Buying.id_prod, Buying.quantity, Buying.unit_price).filter(
        and_(
            Buying.id_store == id_store,
            Buying.id_customer == id_customer
        )
    ).all()
    for product in all_products:
        (id_product, quantity, unit_price) = product
        total_price += unit_price * quantity
        products_bought.append([id_product, quantity])

    return total_price, products_bought


def put_in_history(id_store, id_customer):
    """
    Put all purchases of the customer in the history_customers table

    :param Integer id_store: The id of the store
    :param Integer id_customer: he id of the customer
    :return: None
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    rows_products_bought = s.query(Buying).with_entities(Buying.id_prod, Buying.quantity).filter(
        and_(
            Buying.id_store == id_store,
            Buying.id_customer == id_customer
        )
    ).all()
    for id_prod, quantity in rows_products_bought:
        purchases = HistoryCustomer(date=dt_string, id_customer=id_customer, id_store=id_store, id_prod=id_prod,
                                    quantity=quantity)
        s.add(purchases)
        s.commit()
    s.close


def delete_purchases_customer(id_store, id_customer):
    """
    Delete all lines in the buying table for the (id_store, id_customer) table

    :param Integer id_store: The id of the store
    :param Integer id_customer: he id of the customer
    :return: None
    """
    s.query(Buying).filter(
        and_(
            Buying.id_store == id_store,
            Buying.id_customer == id_customer
        )
    ).delete()
    s.commit()


def change_to_false_in_is_in_store(id_store, id_customer):
    """
    Change to false the is_in value for a given id_store and a given id_customer.

    :param Integer id_store: The id of the store
    :param Integer id_customer: The id of the customer who enters in the store
    :return: None
    """

    change_isin = s.query(IsInStore).filter(
        and_(
            IsInStore.id_store == id_store,
            IsInStore.id_customer == id_customer
        )
    ).first()
    change_isin.is_in = False
    s.commit()
    s.close()


def leave_the_store(id_store, id_customer):
    """
    Orchestrate all action when the client live the score and return the total price of his purchases

    :param Integer id_store: The id of the store
    :param Integer id_customer: he id of the customer
    :return: Total price of purchases
    :rtype: float
    """
    total_price, purchases = compute_total_price(id_store, id_customer)
    for id_product, quantity in purchases:
        change_stock(id_store, id_product, quantity)
    put_in_history(id_store, id_customer)
    delete_purchases_customer(id_store, id_customer)
    change_to_false_in_is_in_store(id_store, id_customer)

    return total_price
