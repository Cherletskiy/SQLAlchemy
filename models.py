import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", backref='publisher', cascade="all, delete", lazy="joined")

    def __str__(self):
        return f"Publisher(id={self.id}, name='{self.name}')"


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))

    stocks = relationship("Stock", backref='book', cascade="all, delete", lazy="joined")

    def __str__(self):
        return f"Book(id={self.id}, title='{self.title}', id_publisher={self.id_publisher})"


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    stocks = relationship("Stock", backref='shop', cascade="all, delete", lazy="joined")

    def __str__(self):
        return f"Shop(id={self.id}, name='{self.name}')"


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    id_shop = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer, nullable=False)

    sales = relationship("Sale", backref='stock', cascade="all, delete", lazy="joined")

    def __str__(self):
        return f"Stock(id={self.id}, id_book={self.id_book}, id_shop={self.id_shop}, count={self.count})"


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(String, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer, nullable=False)

    def __str__(self):
        return f"Sale(id={self.id}, price={self.price}, date_sale={self.date_sale}, id_stock={self.id_stock}, count={self.count})"


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
