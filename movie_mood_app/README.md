# Movie Mood App

Простой учебный проект на `FastAPI`: пользователь входит через Google, пишет своё настроение, получает рекомендацию фильма от GigaChat API и видит историю своих запросов.

## Что умеет приложение

- вход через Google OAuth 2.0
- сохранение пользователя по email
- форма для ввода настроения
- запрос к GigaChat API для подбора фильма
- fallback-рекомендация, если GigaChat недоступен
- сохранение истории в SQLite через SQLAlchemy
- отображение результата и страницы истории через Jinja2

## Структура проекта

```text
movie_mood_app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── gigachat_client.py
├── requirements.txt
├── .env.example
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── result.html
│   └── history.html
└── README.md
```

## 1. Установка зависимостей

Перейдите в папку проекта:

```bash
cd movie_mood_app
```

Создайте виртуальное окружение:

```bash
python3 -m venv .venv
```

Активируйте его:

```bash
source .venv/bin/activate
```

Установите зависимости:

```bash
python3 -m pip install -r requirements.txt
```

## 2. Создание файла `.env`

Скопируйте пример:

```bash
cp .env.example .env
```

Откройте файл `.env` и заполните значения:

```env
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
GIGACHAT_AUTH_KEY=
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_API_URL=https://gigachat.devices.sberbank.ru/api/v1/chat/completions
GIGACHAT_TOKEN_URL=https://ngw.devices.sberbank.ru:9443/api/v2/oauth
SECRET_KEY=
```

### Что означает каждая переменная

- `GOOGLE_CLIENT_ID` и `GOOGLE_CLIENT_SECRET` нужны для входа через Google.
- `GOOGLE_REDIRECT_URI` должен совпадать с адресом callback в настройках Google.
- `GIGACHAT_AUTH_KEY` нужен для получения `access_token` GigaChat.
- `GIGACHAT_SCOPE` обычно равен `GIGACHAT_API_PERS`.
- `GIGACHAT_API_URL` - адрес метода chat/completions.
- `GIGACHAT_TOKEN_URL` - адрес OAuth-метода для получения токена.
- `SECRET_KEY` нужен для сессии FastAPI.

Для `SECRET_KEY` можно сгенерировать строку так:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 3. Где получить Google Client ID и Client Secret

1. Зайдите в [Google Cloud Console](https://console.cloud.google.com/).
2. Создайте новый проект или выберите существующий.
3. Откройте раздел `APIs & Services` -> `OAuth consent screen`.
4. Настройте экран согласия.
5. Если проект в режиме `Testing`, добавьте свой Google-аккаунт в список test users.
6. Перейдите в `APIs & Services` -> `Credentials`.
7. Нажмите `Create Credentials` -> `OAuth client ID`.
8. Выберите тип `Web application`.
9. В `Authorized redirect URIs` добавьте:

```text
http://localhost:8000/auth/callback
```

10. Сохраните и скопируйте `Client ID` и `Client Secret` в `.env`.

Важно: адрес в `Authorized redirect URIs` должен точно совпадать со значением `GOOGLE_REDIRECT_URI`.

## 4. Где взять GigaChat Auth Key

1. Откройте личный кабинет GigaChat API от Сбера.
2. Создайте проект или выберите существующий.
3. Получите ключ авторизации для OAuth.
4. Вставьте его в `.env` в переменную `GIGACHAT_AUTH_KEY`.

В коде реальные ключи не хранятся. Они должны быть только в вашем локальном `.env`.

## 5. Запуск проекта

Из папки `movie_mood_app` выполните:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
uvicorn main:app --reload
```

После запуска откройте в браузере:

```text
http://localhost:8000/login
```

## 6. Как пользоваться приложением

1. Откройте страницу входа.
2. Нажмите `Войти через Google`.
3. После входа введите своё настроение.
4. Нажмите `Подобрать фильм`.
5. Посмотрите результат.
6. Перейдите в `История`, чтобы увидеть прошлые запросы.

## 7. Как работает проект по шагам

### Авторизация

- Пользователь нажимает кнопку входа.
- FastAPI перенаправляет его на Google.
- После успешного входа Google возвращает пользователя на `/auth/callback`.
- Приложение получает email и создаёт пользователя в базе, если его ещё нет.

### Подбор фильма

- Пользователь вводит текст с описанием настроения.
- Приложение получает `access_token` GigaChat через `GIGACHAT_TOKEN_URL`.
- Затем приложение отправляет настроение в `GIGACHAT_API_URL`.
- GigaChat возвращает один фильм и короткое объяснение.
- Ответ разбирается по строкам: `Название фильма`, `Почему подходит`, `Жанр`, `Настроение после просмотра`.
- Результат сохраняется в таблицу `movie_requests`.

Если GigaChat API недоступен, ключ не указан, закончился лимит или произошла ошибка, приложение не падает. Вместо этого используется локальная fallback-логика: по словам в настроении выбирается один из заранее заданных фильмов.

### История

- На странице `/history` показываются все прошлые запросы текущего пользователя.

## 8. База данных

Приложение автоматически создаёт файл базы данных:

```text
movie_mood.db
```

Там будут две таблицы:

- `users`
- `movie_requests`

## 9. Что можно упростить или улучшить потом

Это специально очень простой учебный проект. Позже можно добавить:

- красивый CSS
- обработку ошибок Google OAuth более подробно
- отдельный файл `crud.py`
- пагинацию истории
- валидацию ответа модели в более строгом формате

Но для первого учебного примера текущей структуры достаточно.
