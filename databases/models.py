from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, and_

Base = declarative_base()


class Store(Base):
    __tablename__ = 'store'
    id_store = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    name_store = Column(String(50))

    def __repr__(self):
        return "<Store(address={}, name_store={}>".format(self.address, self.name_store)


class Customer(Base):
    __tablename__ = 'customer'
    id_customer = Column(Integer, primary_key=True)
    mail = Column(String, default=None)
    last_name = Column(String(15))
    first_name = Column(String(15))

    def __repr__(self):
        return "<Customer(mail={}, last_name={}, first_name={}>".format(self.mail, self.last_name, self.first_name)


class Product(Base):
    __tablename__ = 'product'
    id_product = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    brand = Column(String(60))
    unit_price = Column(Float, nullable=False)

    def __repr__(self):
        return "<Product(name={}, brand={}, unit_price={})>".format(self.name, self.brand, self.unit_price)


class Stock(Base):
    __tablename__ = 'stock'
    id_store = Column(Integer, ForeignKey('store.id_store', ondelete='CASCADE'), primary_key=True)
    id_prod = Column(Integer, ForeignKey('product.id_product', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    supplying = Column(Boolean, default=False)

    def __repr__(self):
        return "<Stock(quantity={}, supplying={}>".format(self.quantity, self.supplying)


class IsInStore(Base):
    __tablename__ = 'is_in_store'
    id_store = Column(Integer, ForeignKey('store.id_store', ondelete='CASCADE'), primary_key=True)
    id_customer = Column(Integer, ForeignKey('customer.id_customer', ondelete='CASCADE'), primary_key=True)
    is_in = Column(Boolean, default=False)

    def __repr__(self):
        return "<IsInStore(is_in={})>".format(self.is_in)


class Buying(Base):
    __tablename__ = 'buying'
    id_store = Column(Integer, ForeignKey('store.id_store', ondelete='CASCADE'), primary_key=True)
    id_customer = Column(Integer, ForeignKey('customer.id_customer', ondelete='CASCADE'), primary_key=True)
    id_prod = Column(Integer, ForeignKey('product.id_product', ondelete='SET NULL'), primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(Float)

    def __repr__(self):
        return "<Buying(quantity={}, unit_price={})>".format(self.quantity, self.unit_price)