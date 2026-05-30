# Импортируем datetime, чтобы автоматически записывать время создания рекомендации.
from datetime import datetime

# Импортируем типы колонок SQLAlchemy для описания таблиц базы данных.
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
# Импортируем relationship, чтобы связать пользователей с их запросами.
from sqlalchemy.orm import relationship

# Импортируем общий Base, от которого наследуются ORM-модели.
from database import Base


# Описываем таблицу пользователей в виде Python-класса.
class User(Base):
    """Пользователь приложения. Для учебного проекта храним только email."""

    # Указываем имя таблицы в SQLite.
    __tablename__ = "users"

    # Создаём числовой id пользователя, который является первичным ключом.
    id = Column(Integer, primary_key=True, index=True)
    # Создаём email: он обязателен, индексируется и не может повторяться у разных пользователей.
    email = Column(String, unique=True, index=True, nullable=False)

    # Описываем связь один-ко-многим: у пользователя может быть много запросов фильмов.
    movie_requests = relationship("MovieRequest", back_populates="user")


# Описываем таблицу истории запросов рекомендаций.
class MovieRequest(Base):
    """История запросов пользователя к сервису рекомендаций."""

    # Указываем имя таблицы в SQLite.
    __tablename__ = "movie_requests"

    # Создаём числовой id записи истории, который является первичным ключом.
    id = Column(Integer, primary_key=True, index=True)
    # Храним id пользователя и связываем его с колонкой users.id.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Храним введённое пользователем настроение как текст.
    mood = Column(Text, nullable=False)
    # Храним название рекомендованного фильма.
    movie_title = Column(String, nullable=False)
    # Храним текстовое объяснение, почему фильм подходит.
    movie_description = Column(Text, nullable=False)
    # Храним дату создания записи; по умолчанию ставится текущее UTC-время.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Описываем обратную связь: каждая запись истории принадлежит одному пользователю.
    user = relationship("User", back_populates="movie_requests")
