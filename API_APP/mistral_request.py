# Lm9Hwqybt4VIQLu9ouGHDuX1sChqx5Xc

from mistralai import Mistral
from datetime import datetime, timedelta
from api_proxy.api_methods import get_everything


API_KEY = '7a5108b3318e4ed2812a864f7e5f8355'


def post_annotation(key_word, api_key):
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    news_data = get_everything(
        api_key=api_key,
        q=key_word,
        w_from=yesterday,
        to=yesterday,
        )
    articles = news_data.get('articles', [])

    if not articles:
        return f"По теме {key_word} не нашлось новостей за последние 24 часа"

    split_menu = ''

    for i, art in enumerate(articles):
        title = art.get('title', 'Без заголовка')
        split_menu += f"Новость {i+1}: {title}"

    client = Mistral(api_key='Lm9Hwqybt4VIQLu9ouGHDuX1sChqx5Xc')

    promt = f"""
    Представь - ты аналитик. Перед тобой список статей на тему "{key_word}".

    {split_menu}

    Напиши аннотацию на русском языке аннотацию от 250 до 300 слов.
    Обязательно учти критерии:
    1) Проанализируй основные события за последние 24 часа
    2) Дай свою оценку
    3) Сделай вывод
    """
    chat_response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": promt}]
    )

    return chat_response.choices[0].message.content
