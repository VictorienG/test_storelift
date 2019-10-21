from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean, PrimaryKeyConstraint


Base = declarative_base()


class Store(Base):
    __tablename__ = 'store'
    id_store = Column(Integer, primary_key=True)
    id_product = Column(Integer)
    stock = Column(Integer)
    supplying = Column(Boolean)

    def __repr__(self):
        return "<Store(stock ={}, supplying = {})>".format(self.stock)


