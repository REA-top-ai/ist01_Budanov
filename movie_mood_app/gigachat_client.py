# Импортируем os, чтобы читать настройки GigaChat из переменных окружения.
import os
# Импортируем uuid, чтобы создавать уникальный RqUID для OAuth-запроса к GigaChat.
import uuid

# Импортируем requests, чтобы отправлять HTTP-запросы к GigaChat API.
import requests
# Импортируем urllib3, чтобы при необходимости отключить предупреждения о SSL.
import urllib3
# Импортируем load_dotenv, чтобы локальные настройки из .env стали доступны этому модулю.
from dotenv import load_dotenv

# Импортируем Pydantic-схему результата рекомендации фильма.
from schemas import MovieRecommendation

# Загружаем переменные окружения из .env при импорте модуля.
load_dotenv()


# Определяем функцию, которая решает, проверять ли SSL-сертификат при запросах.
def _verify_ssl() -> bool:
    """Возвращает настройку проверки SSL для запросов к GigaChat."""
    # Читаем GIGACHAT_VERIFY_SSL; строка "true" включает проверку SSL, остальные значения выключают.
    verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL", "false").strip().lower() == "true"
    # Если проверка SSL выключена, нужно убрать шумные предупреждения urllib3 в консоли.
    if not verify_ssl:
        # Отключаем предупреждения InsecureRequestWarning для запросов verify=False.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Возвращаем булево значение, которое потом передаётся в requests.post(..., verify=...).
    return verify_ssl


# Определяем общий обработчик HTTP-ошибок для запросов к GigaChat.
def _raise_for_status(response: requests.Response, action: str) -> None:
    """Пробрасывает HTTP-ошибку с телом ответа, чтобы fallback не скрывал причину."""
    # Пытаемся проверить HTTP-статус ответа.
    try:
        # requests выбросит HTTPError, если статус ответа 4xx или 5xx.
        response.raise_for_status()
    # Перехватываем HTTPError, чтобы добавить к ошибке тело ответа сервера.
    except requests.HTTPError as exc:
        # Берём первые 1000 символов ответа, чтобы не печатать слишком большой текст.
        response_text = response.text[:1000] if response.text else ""
        # Превращаем ошибку в RuntimeError с понятным описанием действия, статуса и тела ответа.
        raise RuntimeError(
            # Формируем строку ошибки для логов и страницы ошибки.
            f"{action} failed: status={response.status_code}, body={response_text}"
        ) from exc


# Определяем функцию разбора текстового ответа GigaChat в структурированные поля.
def _parse_response(text: str) -> MovieRecommendation:
    """
    Разбирает ответ GigaChat по строкам.
    Мы просим строгий формат, поэтому ищем нужные поля по префиксам.
    """
    # Создаём переменную для названия фильма.
    title = ""
    # Создаём переменную для объяснения, почему фильм подходит.
    why = ""
    # Создаём переменную для жанра фильма.
    genre = ""
    # Создаём переменную для настроения после просмотра.
    after = ""
    # Запоминаем первую непустую строку как запасной вариант названия.
    first_non_empty_line = ""

    # Проходим по каждой строке текстового ответа модели.
    for raw_line in text.splitlines():
        # Убираем пробелы по краям текущей строки.
        line = raw_line.strip()
        # Пропускаем пустые строки, потому что в них нет полезных данных.
        if not line:
            # Переходим к следующей строке ответа.
            continue
        # Если первая непустая строка ещё не сохранена, используем текущую.
        if not first_non_empty_line:
            # Сохраняем строку для fallback-названия.
            first_non_empty_line = line

        # Убираем возможный маркер списка, если модель ответила строками вида "- Название фильма: ...".
        line = line.lstrip("-• ").strip()

        # Переводим строку в нижний регистр, чтобы сравнение префиксов не зависело от регистра.
        lower_line = line.lower()
        # Проверяем, содержит ли строка поле названия фильма.
        if lower_line.startswith("название фильма:"):
            # Берём часть после первого двоеточия и сохраняем как название.
            title = line.split(":", 1)[1].strip()
        # Проверяем, содержит ли строка объяснение выбора фильма.
        elif lower_line.startswith("почему подходит:"):
            # Берём текст после двоеточия и сохраняем как объяснение.
            why = line.split(":", 1)[1].strip()
        # Проверяем, содержит ли строка жанр.
        elif lower_line.startswith("жанр:"):
            # Берём текст после двоеточия и сохраняем как жанр.
            genre = line.split(":", 1)[1].strip()
        # Проверяем, содержит ли строка настроение после просмотра.
        elif lower_line.startswith("настроение после просмотра:"):
            # Берём текст после двоеточия и сохраняем как ожидаемое настроение.
            after = line.split(":", 1)[1].strip()

    # Проверяем, удалось ли найти название по строгому префиксу.
    if not title:
        # Если название не найдено, используем первую непустую строку или понятную заглушку.
        title = first_non_empty_line or "Не удалось распознать название фильма"

    # Создаём список частей описания, чтобы собрать его только из реально найденных полей.
    description_parts = []
    # Если есть объяснение, добавляем его в описание.
    if why:
        # Добавляем строку с причиной выбора фильма.
        description_parts.append(f"Почему подходит: {why}")
    # Если есть жанр, добавляем его в описание.
    if genre:
        # Добавляем строку с жанром.
        description_parts.append(f"Жанр: {genre}")
    # Если есть настроение после просмотра, добавляем его в описание.
    if after:
        # Добавляем строку с ожидаемым состоянием после просмотра.
        description_parts.append(f"Настроение после просмотра: {after}")

    # Склеиваем найденные части описания переносами строк или используем исходный текст, если поля не распознаны.
    description = "\n".join(description_parts) if description_parts else text.strip()
    # Возвращаем структурированную рекомендацию в формате MovieRecommendation.
    return MovieRecommendation(movie_title=title, movie_description=description)


# Определяем локальный запасной подбор фильма на случай недоступности GigaChat.
def _fallback_recommendation(mood: str) -> MovieRecommendation:
    """Возвращает локальную рекомендацию, если GigaChat недоступен."""
    # Приводим настроение к нижнему регистру для простого поиска ключевых слов.
    mood_lower = mood.lower()

    # Проверяем ключевые слова грустного или одинокого настроения.
    if any(word in mood_lower for word in ("груст", "плохо", "одинок")):
        # Выбираем фильм для мягкой поддержки.
        title = "1+1"
        # Объясняем, почему фильм подходит.
        why = "Добрый фильм о дружбе, поддержке и возвращении интереса к жизни."
        # Указываем жанр фильма.
        genre = "Драма, комедия"
        # Указываем ожидаемое настроение после просмотра.
        after = "Тепло и надежда"
    # Проверяем слова, связанные с мотивацией, ленью и нехваткой сил.
    elif any(word in mood_lower for word in ("мотивац", "лень", "сил")):
        # Выбираем мотивационный фильм.
        title = "Рокки"
        # Объясняем выбор через тему дисциплины и цели.
        why = "История про дисциплину, упорство и движение к цели маленькими шагами."
        # Указываем жанр фильма.
        genre = "Спортивная драма"
        # Указываем ожидаемый эффект после просмотра.
        after = "Мотивация действовать"
    # Проверяем слова про спокойствие, уют и атмосферность.
    elif any(word in mood_lower for word in ("спокой", "уют", "атмосфер")):
        # Выбираем атмосферный спокойный фильм.
        title = "Амели"
        # Объясняем выбор через лёгкость и визуальный стиль.
        why = "Лёгкий атмосферный фильм с мягким юмором и уютным визуальным стилем."
        # Указываем жанр фильма.
        genre = "Романтическая комедия"
        # Указываем ожидаемое настроение после просмотра.
        after = "Спокойствие и светлая улыбка"
    # Проверяем слова, связанные со страхом и ужасами.
    elif any(word in mood_lower for word in ("страш", "ужас")):
        # Выбираем фильм ужасов.
        title = "Заклятие"
        # Объясняем, что фильм подходит для желания испугаться.
        why = "Напряжённый хоррор для настроения, когда хочется испугаться."
        # Указываем жанр фильма.
        genre = "Ужасы"
        # Указываем ожидаемый эффект после просмотра.
        after = "Адреналин и напряжение"
    # Если ключевые слова не совпали, используем универсальную рекомендацию.
    else:
        # Выбираем фильм по умолчанию.
        title = "Форрест Гамп"
        # Объясняем универсальность выбора.
        why = "Универсальная история о жизни, выборе, доброте и стойкости."
        # Указываем жанр фильма.
        genre = "Драма, комедия"
        # Указываем ожидаемое настроение после просмотра.
        after = "Вдохновение и спокойная грусть"

    # Собираем описание в том же формате, в котором ожидается ответ GigaChat.
    description = (
        # Добавляем причину выбора.
        f"Почему подходит: {why}\n"
        # Добавляем жанр.
        f"Жанр: {genre}\n"
        # Добавляем ожидаемое настроение после просмотра.
        f"Настроение после просмотра: {after}"
    )
    # Возвращаем рекомендацию в общей Pydantic-схеме.
    return MovieRecommendation(movie_title=title, movie_description=description)


# Определяем функцию получения OAuth access_token для GigaChat API.
def _get_access_token() -> str:
    """Получает access_token GigaChat через OAuth-запрос Сбера."""
    # Читаем авторизационный ключ GigaChat из .env.
    auth_key = os.getenv("GIGACHAT_AUTH_KEY")
    # Читаем scope GigaChat или используем персональный API scope по умолчанию.
    scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    # Читаем URL выдачи токена или используем стандартный OAuth endpoint GigaChat.
    token_url = os.getenv("GIGACHAT_TOKEN_URL", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth")
    # Получаем настройку проверки SSL для HTTP-запроса.
    verify_ssl = _verify_ssl()

    # Печатаем, найден ли auth key, не раскрывая сам секрет.
    print("GIGACHAT_AUTH_KEY loaded:", bool(auth_key))
    # Печатаем используемый scope для диагностики настройки.
    print("GIGACHAT_SCOPE:", scope)
    # Печатаем URL получения токена для диагностики.
    print("GIGACHAT_TOKEN_URL:", token_url)
    # Печатаем настройку SSL-проверки для диагностики.
    print("GIGACHAT_VERIFY_SSL:", verify_ssl)

    # Проверяем, задан ли обязательный ключ авторизации.
    if not auth_key:
        # Прерываем работу с понятной ошибкой, если ключ отсутствует.
        raise ValueError("GIGACHAT_AUTH_KEY не найден в .env.")

    # Отправляем OAuth-запрос на получение access_token.
    response = requests.post(
        # Передаём адрес OAuth endpoint.
        token_url,
        # Передаём HTTP-заголовки, которые требует GigaChat OAuth.
        headers={
            # Basic-токен авторизации из .env.
            "Authorization": f"Basic {auth_key}",
            # Указываем формат тела запроса как HTML form.
            "Content-Type": "application/x-www-form-urlencoded",
            # Просим ответ в JSON.
            "Accept": "application/json",
            # Передаём уникальный идентификатор запроса.
            "RqUID": str(uuid.uuid4()),
        },
        # Передаём scope в теле формы.
        data={"scope": scope},
        # Ограничиваем ожидание ответа двадцатью секундами.
        timeout=20,
        # Передаём настройку проверки SSL.
        verify=verify_ssl,
    )
    # Проверяем HTTP-статус и выбрасываем понятную ошибку при 4xx/5xx.
    _raise_for_status(response, "GigaChat OAuth token request")

    # Разбираем JSON-ответ с токеном.
    token_data = response.json()
    # Достаём access_token из JSON.
    access_token = token_data.get("access_token")
    # Проверяем, что токен действительно пришёл.
    if not access_token:
        # Прерываем работу, если формат ответа не содержит access_token.
        raise ValueError("GigaChat не вернул access_token.")

    # Возвращаем токен для последующего запроса к chat/completions.
    return access_token


# Определяем функцию, которая отправляет настроение пользователя в GigaChat.
def _request_gigachat(mood: str) -> str:
    """Отправляет настроение в GigaChat и возвращает текст ответа модели."""
    # Читаем URL chat/completions API или используем стандартный endpoint GigaChat.
    api_url = os.getenv(
        # Имя переменной окружения для переопределения API URL.
        "GIGACHAT_API_URL",
        # Значение по умолчанию для GigaChat API.
        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
    )
    # Получаем настройку проверки SSL для запроса.
    verify_ssl = _verify_ssl()
    # Получаем OAuth access_token перед обращением к модели.
    access_token = _get_access_token()

    # Формируем пользовательский prompt со строгим форматом ответа.
    prompt = f"""Пользователь описал своё настроение: {mood}.
Подбери один фильм, который подойдёт под это настроение.
Ответь строго в формате:
Название фильма: ...
Почему подходит: ...
Жанр: ...
Настроение после просмотра: ..."""

    # Отправляем запрос к GigaChat chat/completions.
    response = requests.post(
        # Передаём URL API модели.
        api_url,
        # Передаём заголовки авторизации и формата данных.
        headers={
            # Передаём access_token в Bearer-авторизации.
            "Authorization": f"Bearer {access_token}",
            # Сообщаем, что тело запроса отправляется как JSON.
            "Content-Type": "application/json",
            # Просим ответ в формате JSON.
            "Accept": "application/json",
        },
        # Передаём JSON-тело запроса к модели.
        json={
            # Указываем модель GigaChat.
            "model": "GigaChat",
            # Передаём диалоговые сообщения для модели.
            "messages": [
                # Первое сообщение задаёт роль и правила ответа ассистента.
                {
                    # Роль system задаёт общие инструкции модели.
                    "role": "system",
                    # Контент объясняет модели задачу и ограничивает формат ответа.
                    "content": (
                        # Первая часть инструкции задаёт роль помощника по фильмам.
                        "Ты помогаешь подобрать один подходящий фильм по настроению. "
                        # Вторая часть требует русский язык и строгий формат.
                        "Отвечай только на русском языке и только в указанном формате."
                    ),
                },
                # Второе сообщение передаёт конкретное настроение пользователя.
                {"role": "user", "content": prompt},
            ],
            # Устанавливаем температуру, чтобы ответы были немного разнообразными.
            "temperature": 0.8,
        },
        # Ограничиваем ожидание ответа сорока секундами.
        timeout=40,
        # Передаём настройку проверки SSL.
        verify=verify_ssl,
    )
    # Проверяем HTTP-статус ответа GigaChat.
    _raise_for_status(response, "GigaChat chat/completions request")

    # Разбираем JSON-ответ модели.
    data = response.json()
    # Пробуем достать текст ответа из стандартной структуры choices[0].message.content.
    try:
        # Возвращаем текст ответа или пустую строку, если content равен None.
        return data["choices"][0]["message"]["content"] or ""
    # Ловим ошибки структуры JSON, если GigaChat вернул неожиданный формат.
    except (KeyError, IndexError, TypeError) as exc:
        # Прерываем работу с диагностикой всего ответа.
        raise ValueError(f"Unexpected GigaChat response format: {data}") from exc


# Определяем публичную функцию, которую вызывает main.py для получения фильма.
def get_movie_recommendation(mood: str) -> MovieRecommendation:
    """
    Возвращает рекомендацию фильма по настроению.
    Если GigaChat недоступен или ключ не настроен, используется локальный fallback.
    """
    # Пробуем получить рекомендацию через реальный GigaChat API.
    try:
        # Отправляем настроение в GigaChat и получаем сырой текст ответа.
        message_text = _request_gigachat(mood)
        # Разбираем сырой текст в MovieRecommendation.
        return _parse_response(message_text)
    # Если любая часть интеграции упала, не ломаем приложение для пользователя.
    except Exception as exc:
        # Печатаем техническую ошибку в консоль сервера для диагностики.
        print("GIGACHAT ERROR:", repr(exc))
        # Возвращаем локальную рекомендацию по ключевым словам.
        return _fallback_recommendation(mood)
