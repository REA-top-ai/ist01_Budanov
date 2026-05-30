# Импортируем datetime, чтобы типизировать дату создания записи в схемах ответа.
from datetime import datetime

# Импортируем BaseModel для Pydantic-схем, ConfigDict для настройки ORM-чтения и Field для валидации.
from pydantic import BaseModel, ConfigDict, Field


# Описываем данные, которые пользователь вводит в форму настроения.
class MoodInput(BaseModel):
    """Данные, которые пользователь вводит в форму."""

    # Поле mood обязательно и должно содержать минимум один символ.
    mood: str = Field(..., min_length=1)


# Описываем структуру рекомендации, которую возвращает модуль подбора фильма.
class MovieRecommendation(BaseModel):
    """Результат, который приходит после обработки запроса к GigaChat."""

    # Название фильма, выбранного под настроение пользователя.
    movie_title: str
    # Текстовое описание: почему подходит, жанр и ожидаемое настроение после просмотра.
    movie_description: str


# Описываем схему чтения одной записи истории, расширяя схему рекомендации.
class MovieRequestRead(MovieRecommendation):
    """Схема одной записи истории запросов."""

    # Разрешаем Pydantic создавать объект схемы из SQLAlchemy ORM-объекта.
    model_config = ConfigDict(from_attributes=True)

    # id записи истории в базе данных.
    id: int
    # Исходное настроение, которое вводил пользователь.
    mood: str
    # Дата и время создания записи истории.
    created_at: datetime
