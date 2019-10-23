from sqlalchemy import and_

from databases.crud import s
from databases.models import Stock, IsInStore, Buying


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
    )
    change_quantity_stock.quantity = change_quantity_stock.quantity - quantity_bought
    s.commit()
    s.close()


def compute_total_price(id_store, id_customer):
    """
    Compute the total price for a customer and return all products bought with their corresponding quantity.

    :param Integer id_store:
    :param Integer id_customer:
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

    return (total_price, products_bought)


def customer_leave_the_store(id_store, id_customer):
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


# mettre dans historique

