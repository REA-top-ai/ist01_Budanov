# Импортируем create_engine, чтобы создать подключение SQLAlchemy к базе данных.
from sqlalchemy import create_engine
# Импортируем declarative_base для базового класса моделей и sessionmaker для фабрики сессий.
from sqlalchemy.orm import declarative_base, sessionmaker

# Указываем адрес SQLite-базы: файл movie_mood.db лежит в корне проекта.
DATABASE_URL = "sqlite:///./movie_mood.db"

# Создаём engine SQLAlchemy, через который приложение физически общается с SQLite.
engine = create_engine(
    # Передаём строку подключения к базе данных.
    DATABASE_URL,
    # Отключаем ограничение SQLite на использование соединения только в одном потоке.
    connect_args={"check_same_thread": False},
)

# Создаём фабрику SessionLocal, которая будет выдавать отдельную сессию БД на запрос.
SessionLocal = sessionmaker(
    # Отключаем автоматический commit, чтобы явно сохранять изменения через db.commit().
    autocommit=False,
    # Отключаем автоматический flush, чтобы изменения отправлялись в БД контролируемо.
    autoflush=False,
    # Привязываем сессии к созданному engine.
    bind=engine,
)

# Создаём базовый класс, от которого наследуются все ORM-модели проекта.
Base = declarative_base()


# Определяем зависимость FastAPI для выдачи сессии базы данных в маршруты.
def get_db():
    """Отдаёт сессию базы данных и закрывает её после запроса."""
    # Создаём новую сессию базы данных для конкретного HTTP-запроса.
    db = SessionLocal()
    # Начинаем блок, который гарантирует закрытие сессии после использования.
    try:
        # Отдаём сессию вызывающему маршруту FastAPI.
        yield db
    # Блок finally выполнится даже при ошибке внутри маршрута.
    finally:
        # Закрываем сессию, чтобы не держать лишнее соединение с базой.
        db.close()
