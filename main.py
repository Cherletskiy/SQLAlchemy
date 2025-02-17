import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
import models
from tabulate import tabulate


from models import create_tables, Book, Publisher, Shop, Stock, Sale

DSN = "sqlite:///db.db"
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_test_data(file) -> None:
    """Функция заполните БД тестовыми данными.
    На вход принимает json-файл и добавляет данные в БД.
    """
    with open(file) as f:
        json_data = json.load(f)
        for i in json_data:
            model_class = getattr(models, i['model'].capitalize(), None)
            if model_class:
                obj = model_class(id=i['pk'], **i['fields'])
                session.add(obj)
        session.commit()


def get_sale_data() -> None:
    """Функция принимает имя или идентификатор издателя (publisher) через input().
    Выводит построчно факты покупки книг этого издателя
    """
    inp_str = input("Укажите имя или идентификатор издателя (publisher): ")

    if inp_str.isdigit():
        pub_filter = Publisher.id == int(inp_str)
    else:
        pub_filter = Publisher.name == inp_str

    q = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
         .join(Stock, Sale.id_stock == Stock.id)
         .join(Book, Stock.id_book == Book.id)
         .join(Shop, Stock.id_shop == Shop.id)
         .join(Publisher, Book.id_publisher == Publisher.id)
         .filter(pub_filter)
         .all()
         )

    if q:
        headers = ["Title", "Shop", "Price", "Date"]
        print("Результаты:")
        print(tabulate(q, headers=headers, tablefmt="grid"))
    else:
        print("Ничего не найдено.")


# add_test_data("tests_data.json")

get_sale_data()

session.close()





