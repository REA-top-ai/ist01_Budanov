# Импортируем os, чтобы читать OAuth-настройки из переменных окружения.
import os
# Импортируем Path, чтобы собрать путь к папке HTML-шаблонов.
from pathlib import Path

# Импортируем OAuth-клиент Authlib для работы с Google OAuth.
from authlib.integrations.starlette_client import OAuth
# Импортируем загрузчик .env, чтобы локальные переменные окружения были доступны приложению.
from dotenv import load_dotenv
# Импортируем инструменты FastAPI для роутера, зависимостей и запроса.
from fastapi import APIRouter, Depends, Request
# Импортируем RedirectResponse, чтобы перенаправлять пользователя после входа и выхода.
from fastapi.responses import RedirectResponse
# Импортируем Jinja2Templates, чтобы отдавать HTML-страницу входа.
from fastapi.templating import Jinja2Templates
# Импортируем Session, чтобы типизировать подключение к базе данных.
from sqlalchemy.orm import Session

# Импортируем зависимость получения сессии базы данных.
from database import get_db
# Импортируем модель пользователя для поиска и создания аккаунта.
from models import User

load_dotenv()  # Загружаем переменные окружения из файла .env.

# Блок объектов авторизации рассчитан на маршруты входа через Google.
router = APIRouter()  # Создаём отдельный роутер для auth-маршрутов.
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))  # Настраиваем папку HTML-шаблонов.
oauth = OAuth()  # Создаём объект OAuth, в который позже регистрируется Google-клиент.


# Функция регистрации Google рассчитана на ленивую настройку OAuth-клиента.
def _register_google_if_needed():
    """
    Регистрирует Google OAuth-клиент.
    Делаем это отдельно, чтобы приложение не падало при пустом .env.
    """
    if oauth.create_client("google"):  # Проверяем, зарегистрирован ли клиент Google уже сейчас.
        return  # Выходим, если повторная регистрация не нужна.

    client_id = os.getenv("GOOGLE_CLIENT_ID")  # Читаем Google Client ID из переменных окружения.
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")  # Читаем Google Client Secret из переменных окружения.

    if client_id and client_secret:  # Регистрируем OAuth-клиент только если есть оба обязательных значения.
        oauth.register(  # Добавляем Google как провайдера OAuth.
            name="google",  # Указываем внутреннее имя клиента.
            client_id=client_id,  # Передаём Google Client ID.
            client_secret=client_secret,  # Передаём Google Client Secret.
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",  # Используем стандартную OpenID-конфигурацию Google.
            client_kwargs={"scope": "openid email profile"},  # Запрашиваем профиль, email и OpenID.
        )  # Завершаем регистрацию Google-клиента.


# Функция рассчитана на получение пользователя, который уже вошёл в приложение.
def get_current_user(request: Request, db: Session) -> User | None:
    """Ищет пользователя в сессии и возвращает его из базы данных."""
    user_email = request.session.get("user_email")  # Достаём email пользователя из cookie-сессии.
    if not user_email:  # Проверяем, есть ли email в сессии.
        return None  # Возвращаем None, если пользователь не вошёл.
    return db.query(User).filter(User.email == user_email).first()  # Ищем пользователя в базе по email.


# Маршрут страницы входа рассчитан на показ кнопки Google и возможной ошибки настройки.
@router.get("/login")
async def login_page(request: Request):
    """Страница с кнопкой входа через Google."""
    config_error = None  # По умолчанию считаем, что ошибки настройки OAuth нет.

    if not os.getenv("GOOGLE_CLIENT_ID") or not os.getenv("GOOGLE_CLIENT_SECRET"):  # Проверяем наличие Google OAuth-настроек.
        config_error = "Сначала заполните GOOGLE_CLIENT_ID и GOOGLE_CLIENT_SECRET в файле .env."  # Готовим сообщение об ошибке настройки.

    return templates.TemplateResponse(  # Возвращаем HTML-страницу входа.
        request,
        "login.html",  # Используем шаблон страницы входа.
        {  # Собираем контекст для шаблона.
            "request": request,  # Передаём объект запроса для Jinja2Templates.
            "config_error": config_error,  # Передаём ошибку настройки или None.
            "user_email": request.session.get("user_email"),  # Передаём email из сессии, если пользователь уже вошёл.
        },  # Завершаем словарь контекста.
    )  # Завершаем возврат страницы входа.


# Маршрут авторизации рассчитан на перенаправление пользователя в Google.
@router.get("/auth/google")
async def auth_google(request: Request):
    """Перенаправляет пользователя на страницу входа Google."""
    _register_google_if_needed()  # Гарантируем, что Google-клиент зарегистрирован при наличии настроек.
    google = oauth.create_client("google")  # Получаем зарегистрированный OAuth-клиент Google.

    if not google:  # Проверяем, получилось ли создать Google-клиент.
        return templates.TemplateResponse(  # Возвращаем страницу входа с ошибкой настройки.
            request,
            "login.html",  # Используем шаблон входа.
            {  # Собираем контекст ошибки.
                "request": request,  # Передаём объект запроса.
                "config_error": "Google OAuth не настроен. Проверьте переменные окружения в .env.",  # Показываем причину проблемы.
                "user_email": request.session.get("user_email"),  # Передаём email из сессии, если он есть.
            },  # Завершаем словарь контекста.
            status_code=400,  # Возвращаем код 400 из-за некорректной настройки.
        )  # Завершаем возврат страницы с ошибкой OAuth.

    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")  # Берём callback URL из .env или используем локальный.
    return await google.authorize_redirect(request, redirect_uri)  # Перенаправляем пользователя на страницу входа Google.


# Callback-маршрут рассчитан на обработку ответа Google после успешного входа.
@router.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    """Обрабатывает ответ от Google, сохраняет email и создаёт пользователя в БД."""
    _register_google_if_needed()  # Проверяем регистрацию Google-клиента перед обработкой callback.
    google = oauth.create_client("google")  # Получаем OAuth-клиент Google.

    if not google:  # Проверяем, доступен ли Google-клиент.
        return RedirectResponse(url="/login")  # Возвращаем пользователя на вход, если OAuth не настроен.

    token = await google.authorize_access_token(request)  # Обмениваем callback от Google на access token.
    user_info = token.get("userinfo")  # Пробуем взять данные пользователя прямо из токена.

    if not user_info:  # Проверяем, пришла ли информация о пользователе в токене.
        user_info = await google.parse_id_token(request, token)  # Разбираем id_token, если userinfo не было.

    email = user_info.get("email") if user_info else None  # Достаём email из данных пользователя.
    if not email:  # Проверяем, удалось ли получить email.
        return RedirectResponse(url="/login")  # Возвращаем на вход, если email отсутствует.

    user = db.query(User).filter(User.email == email).first()  # Ищем пользователя с таким email в базе.
    if not user:  # Проверяем, нужно ли создать нового пользователя.
        user = User(email=email)  # Создаём ORM-объект пользователя.
        db.add(user)  # Добавляем пользователя в сессию базы данных.
        db.commit()  # Сохраняем нового пользователя в базе.
        db.refresh(user)  # Обновляем объект, чтобы получить его id.

    # Сохраняем email в сессии, чтобы знать, кто вошёл в приложение.
    request.session["user_email"] = user.email  # Записываем email в cookie-сессию пользователя.
    return RedirectResponse(url="/", status_code=302)  # Перенаправляем вошедшего пользователя на главную.


# Маршрут выхода рассчитан на очистку сессии пользователя.
@router.get("/logout")
async def logout(request: Request):
    """Выход из приложения: просто очищаем сессию."""
    request.session.clear()  # Удаляем все данные из текущей сессии.
    return RedirectResponse(url="/login", status_code=302)  # Перенаправляем пользователя на страницу входа.
