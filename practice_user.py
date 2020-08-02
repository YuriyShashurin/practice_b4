import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    """
    структура базы
    """
    __tablename__ = 'user'

    id = sql.Column(sql.Integer, primary_key=True)
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


def add_user():
    """
        берем данные от пользователя и добавляем в список
    """

    first_name = input("Имя?: ")
    last_name = input("Фамилия: ")
    gender = input("Пол?: ")
    email = input("Email: ")
    birthdate = input("Дата рождения(в формате ГГГГ-ММ-ДД): ")
    height = input("Рост в метрах: ")
    user = User(

        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def main():
    """
    Запуск приложения, обработка ввода
    """
    session = connect_db()
    user = add_user()
    session.add(user)
    session.commit()
    print("Запись добавлен")


if __name__ == "__main__":
    main()
