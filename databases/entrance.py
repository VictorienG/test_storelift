from sqlalchemy import and_
from databases.crud import s
from databases.models import Customer, IsInStore


def create_customer(last_name, first_name, mail=None):
    """
    Check if the customer who enter is a new customer. In this case, a new customer is created in the Customer table.

    :param str last_name: The last_name of the customer
    :param str first_name:  The customer's last name
    :param str mail: The mail of the customer
    :return: The id of the customer
    :rtype: str
    """
    id_customer = s.query(Customer).with_entities(Customer.id_customer).filter(
        and_(
            Customer.last_name.ilike(last_name),
            Customer.first_name.ilike(first_name)
        )
    ).all()
    if len(id_customer) == 0:
        new_customer = Customer(mail=mail, last_name=last_name, first_name=first_name)
        s.add(new_customer)
        s.commit()
        id_customer = s.query(Customer).count()
    else:
        id_customer = id_customer[0][0]
    s.close()
    return id_customer


def customer_in_the_store(id_store, id_customer):
    """
    Change to true the is_in value for a given id_store and a given id_customer.
    Create a line in the IsInStore table if the couple (id_store, id_customer) does not exist

    :param int id_store: The id of the store
    :param int id_customer: The id of the customer who enters in the store
    :return: None
    """
    try:
        change_isin = s.query(IsInStore).filter(
            and_(
                IsInStore.id_store == id_store,
                IsInStore.id_customer == id_customer
            )
        ).first()
        change_isin.is_in = True
        s.commit()
    except:
        new_link = IsInStore(id_store=id_store, id_customer=id_customer, is_in=True)
        s.add(new_link)
        s.commit()
    s.close()


def entrance(id_store, last_name, first_name, mail=None):
    """
    Orchestrate all changements in the database when a customer goes into a store. The fucntion returns the customer's
    id.

    :param int id_store: The id of the store
    :param str last_name: The last_name of the customer
    :param str first_name:  The customer's last name
    :param str mail: The mail of the customer
    :return: The customer's id
    :rtype: int
    """
    id_customer = create_customer(last_name, first_name, mail)
    customer_in_the_store(id_store, id_customer)

    return id_customer
