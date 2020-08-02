import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class Athelete(Base):
    """
    Структура базы Athelete
    """
    __tablename__ = 'athelete'

    id = sql.Column(sql.Integer, primary_key=True)
    age = sql.Column(sql.Integer)
    birthdate = sql.Column(sql.Text)
    gender = sql.Column(sql.Text)
    height = sql.Column(sql.Float)
    weight = sql.Column(sql.Integer)
    name = sql.Column(sql.Text)
    gold_medals = sql.Column(sql.Integer)
    silver_medals = sql.Column(sql.Integer)
    bronze_medals = sql.Column(sql.Integer)
    total_medals = sql.Column(sql.Integer)
    sport = sql.Column(sql.Text)
    country = sql.Column(sql.Text)


class User(Base):
    """
    Структура базы user
    """
    __tablename__ = 'user'

    id = sql.Column(sql.String(36), primary_key=True)
    first_name = sql.Column(sql.Text)
    last_name = sql.Column(sql.Text)
    gender = sql.Column(sql.Text)
    email = sql.Column(sql.Text)
    birthdate = sql.Column(sql.Text)
    height = sql.Column(sql.Float)


def connect_db():
    """
    Соединение с баозой
    """

    engine = sql.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_id():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    user_id = input("Ввести идентификатор пользователя: ")
    return int(user_id)


def convert_str_to_date(date_str):
    """
    Конвертирует строку с датой в формате ГГГГ-ММ-ЧЧ в объект  datetime.date, подсмотрел в разборе, иначе не мог понять, почему не так работает скрипт
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def nearest_bd(user, session):
    """
    поиск ближайшего др по айди
    """
    user_birthday = convert_str_to_date(user.birthdate)
    athelete_all = session.query(Athelete).all()
    atheletes_birthday = {athlete.id: convert_str_to_date(athlete.birthdate) for athlete in athelete_all}
    min_abs = None
    near_id = None
    near_birthday = None
    for ids, bd in atheletes_birthday.items():

        minimal = abs(user_birthday-bd)
        if not min_abs or minimal < min_abs:
            min_abs = minimal
            near_id = ids
            near_birthday = bd

    near_name = session.query(Athelete).filter(Athelete.id == near_id).first()

    return "Ближайший по дню рождения {}, айди: {}, дата рождения: {}".format(near_name.name, near_id, near_birthday)


def nearest_height(user, session):
    """
    поиск ближайшего др по айди
    """
    user_height = user.height
    athelete_all = session.query(Athelete).filter(Athelete.height != None).all() ##подсмотрел в разборе
    atheletes_height = {athlete.id: athlete.height for athlete in athelete_all}
    min_abs = None
    near_id = None
    near_height = None
    for ids, height in atheletes_height.items():

        minimal = abs(user_height-height)
        if not min_abs or minimal < min_abs:
            min_abs = minimal
            near_id = ids
            near_height = height

    near_name = session.query(Athelete).filter(Athelete.id == near_id).first()

    return "Ближайший по росту {}, айди: {}, рост: {}".format(near_name.name, near_id, near_height)



def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    user_id = request_id()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        near_bd = nearest_bd(user, session)
        near_height = nearest_height(user, session)
        print(near_bd)
        print(near_height)

    else:
        print("Такого пользователя не нашлось:(")



if __name__ == "__main__":
    main()