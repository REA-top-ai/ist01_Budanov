# Импортируем os, чтобы читать секретный ключ сессий из переменных окружения.
import os
# Импортируем Path, чтобы собрать надёжный путь к папке templates рядом с этим файлом.
from pathlib import Path

# Импортируем load_dotenv, чтобы переменные из .env загрузились при старте приложения.
from dotenv import load_dotenv
# Импортируем Depends для зависимостей, FastAPI для приложения, Form для формы и Request для данных запроса.
from fastapi import Depends, FastAPI, Form, Request
# Импортируем RedirectResponse, чтобы перенаправлять неавторизованных пользователей на страницу входа.
from fastapi.responses import RedirectResponse
# Импортируем Jinja2Templates, чтобы FastAPI мог рендерить HTML-шаблоны.
from fastapi.templating import Jinja2Templates
# Импортируем Session, чтобы типизировать объект подключения к базе данных.
from sqlalchemy.orm import Session
# Импортируем SessionMiddleware, чтобы хранить данные входа пользователя в cookie-сессии.
from starlette.middleware.sessions import SessionMiddleware

# Импортируем функцию получения текущего пользователя и роутер с маршрутами авторизации.
from auth import get_current_user, router as auth_router
# Импортируем Base для создания таблиц, engine для подключения и get_db для сессий базы.
from database import Base, engine, get_db
# Импортируем функцию, которая получает рекомендацию фильма по настроению.
from gigachat_client import get_movie_recommendation
# Импортируем ORM-модель записи запроса фильма, которую сохраняем в историю.
from models import MovieRequest

# Загружаем переменные окружения из .env до настройки приложения и клиентов API.
load_dotenv()

# Создаём таблицы в базе данных при запуске, если их ещё нет.
Base.metadata.create_all(bind=engine)

# Создаём объект FastAPI, который будет принимать HTTP-запросы.
app = FastAPI(title="Movie Mood App")
# Добавляем middleware сессий, чтобы приложение могло помнить вошедшего пользователя между запросами.
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY") or "change-me-in-env")
# Подключаем маршруты авторизации: /login, /auth/google, /auth/callback и /logout.
app.include_router(auth_router)

# Настраиваем папку HTML-шаблонов относительно текущего файла, чтобы запуск из другой директории не ломал пути.
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


# Регистрируем GET-маршрут главной страницы приложения.
@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    """Главная страница с формой для ввода настроения."""
    # Пытаемся найти пользователя по данным из cookie-сессии.
    user = get_current_user(request, db)
    # Если пользователь не найден, значит он не вошёл в приложение.
    if not user:
        # Перенаправляем неавторизованного пользователя на страницу входа.
        return RedirectResponse(url="/login", status_code=302)

    # Возвращаем HTML главной страницы с формой ввода настроения.
    return templates.TemplateResponse(
        # Передаём объект запроса в шаблонизатор, как требует Jinja2Templates.
        request,
        # Указываем файл шаблона, который нужно отрендерить.
        "index.html",
        # Передаём данные, доступные внутри шаблона.
        {
            # Дублируем request в контекст для совместимости шаблонов FastAPI.
            "request": request,
            # Передаём пользователя, чтобы показать его email на странице.
            "user": user,
            # Передаём отсутствие ошибки для первого открытия страницы.
            "error": None,
            # Передаём пустое значение поля настроения для новой формы.
            "mood_value": "",
        },
    )


# Регистрируем POST-маршрут, который принимает отправленную форму настроения.
@app.post("/recommend")
def recommend_movie(
    # Получаем объект HTTP-запроса, чтобы работать с сессией и шаблонами.
    request: Request,
    # Получаем поле mood из HTML-формы; троеточие означает обязательное поле.
    mood: str = Form(...),
    # Получаем сессию базы данных через зависимость FastAPI.
    db: Session = Depends(get_db),
):
    """Получает настроение, отправляет его в GigaChat и сохраняет результат в БД."""
    # Проверяем, какой пользователь сейчас вошёл в приложение.
    user = get_current_user(request, db)
    # Если пользователь не вошёл, не даём сохранять рекомендации без аккаунта.
    if not user:
        # Возвращаем пользователя на страницу входа.
        return RedirectResponse(url="/login", status_code=302)

    # Убираем пробелы и переносы строк по краям введённого настроения.
    cleaned_mood = mood.strip()
    # Проверяем, осталось ли содержательное описание после очистки.
    if not cleaned_mood:
        # Возвращаем главную страницу с ошибкой валидации.
        return templates.TemplateResponse(
            # Передаём request для рендера шаблона.
            request,
            # Показываем тот же шаблон с формой.
            "index.html",
            # Собираем контекст страницы с текстом ошибки.
            {
                # Передаём request в шаблон.
                "request": request,
                # Передаём текущего пользователя.
                "user": user,
                # Передаём сообщение, которое покажется в блоке ошибки.
                "error": "Введите настроение перед отправкой формы.",
                # Оставляем поле формы пустым, потому что введены только пробелы.
                "mood_value": "",
            },
            # Возвращаем HTTP 400, потому что пользователь отправил некорректные данные.
            status_code=400,
        )

    # Пробуем получить рекомендацию через внешний сервис или локальный fallback.
    try:
        # Передаём очищенное настроение в модуль рекомендаций.
        recommendation = get_movie_recommendation(cleaned_mood)
    # Ловим неожиданную ошибку, чтобы приложение показало понятное сообщение вместо падения.
    except Exception as exc:
        # Возвращаем форму с сообщением о проблеме получения рекомендации.
        return templates.TemplateResponse(
            # Передаём request для шаблона.
            request,
            # Снова рендерим главную страницу.
            "index.html",
            # Собираем контекст ошибки.
            {
                # Передаём request в шаблон.
                "request": request,
                # Передаём пользователя, чтобы шапка страницы сохранилась.
                "user": user,
                # Показываем текст ошибки, включая причину из исключения.
                "error": f"Не удалось получить рекомендацию: {exc}",
                # Возвращаем введённое настроение обратно в поле формы.
                "mood_value": cleaned_mood,
            },
            # Возвращаем HTTP 500, потому что сбой произошёл при обработке на сервере.
            status_code=500,
        )

    # Создаём ORM-объект истории запроса для сохранения в SQLite.
    movie_request = MovieRequest(
        # Привязываем запись истории к текущему пользователю.
        user_id=user.id,
        # Сохраняем очищенный текст настроения.
        mood=cleaned_mood,
        # Сохраняем название фильма из ответа рекомендации.
        movie_title=recommendation.movie_title,
        # Сохраняем объяснение рекомендации из ответа.
        movie_description=recommendation.movie_description,
    )
    # Добавляем новую запись в текущую сессию базы данных.
    db.add(movie_request)
    # Фиксируем изменения, чтобы запись реально появилась в файле SQLite.
    db.commit()
    # Обновляем объект из базы, чтобы получить id и created_at после сохранения.
    db.refresh(movie_request)

    # Возвращаем страницу результата с сохранённой рекомендацией.
    return templates.TemplateResponse(
        # Передаём request в шаблонизатор.
        request,
        # Указываем HTML-шаблон результата.
        "result.html",
        # Передаём данные для отображения результата.
        {
            # Передаём request в шаблон.
            "request": request,
            # Передаём пользователя для отображения email.
            "user": user,
            # Передаём сохранённую запись, чтобы показать настроение, фильм и описание.
            "movie_request": movie_request,
        },
    )


# Регистрируем GET-маршрут страницы истории.
@app.get("/history")
def history(request: Request, db: Session = Depends(get_db)):
    """Показывает историю прошлых запросов текущего пользователя."""
    # Получаем текущего пользователя из cookie-сессии и базы данных.
    user = get_current_user(request, db)
    # Если пользователь не вошёл, историю показывать нельзя.
    if not user:
        # Перенаправляем на вход.
        return RedirectResponse(url="/login", status_code=302)

    # Готовим запрос к базе за всеми рекомендациями текущего пользователя.
    history_items = (
        # Начинаем SQLAlchemy-запрос по таблице movie_requests.
        db.query(MovieRequest)
        # Оставляем только записи, принадлежащие текущему пользователю.
        .filter(MovieRequest.user_id == user.id)
        # Сортируем историю от самой новой записи к самой старой.
        .order_by(MovieRequest.created_at.desc())
        # Выполняем запрос и получаем список ORM-объектов.
        .all()
    )

    # Возвращаем HTML-страницу истории.
    return templates.TemplateResponse(
        # Передаём request для рендера шаблона.
        request,
        # Указываем шаблон истории.
        "history.html",
        # Передаём данные страницы.
        {
            # Передаём request в шаблон.
            "request": request,
            # Передаём пользователя для отображения email.
            "user": user,
            # Передаём список записей истории для таблицы.
            "history_items": history_items,
        },
    )
