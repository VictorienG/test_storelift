from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from databases.fill_dbs import fill_store, fill_customer, fill_product, fill_stock, fill_is_in_store
from databases.models import Base

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def recreate_database():
    """
    Delete the old database and create a new databases with all tables named in models
    :return: A database
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def init_databases():
    """
    Fill all tables in the database created in the recreated_database function
    :return: A filled database
    """
    s = Session()
    s.bulk_save_objects(fill_store)
    s.bulk_save_objects(fill_customer)
    s.bulk_save_objects(fill_product)
    s.bulk_save_objects(fill_stock)
    s.bulk_save_objects(fill_is_in_store)
    s.commit()
    s.close()


def pipeline_create_databases():
    """
    Orchestrate the creation of the database
    :return: A filled and new database
    """
    recreate_database()
    init_databases()
