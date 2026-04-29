from api_proxy.api_methods import get_everything


def give_50_filtered_news(q: str, api_key: str) -> list[dict]:
    data = get_everything(
        api_key=api_key,
        q=q,
        sort_by='publishedAt',
        page_size=100
    )
    articles = data.get('articles')
    filtered_articles = []

    for art in articles:
        title = art.get('title')
        url = art.get('url')
        description = art.get('description')

        if title and url and len(description) >= 50:
            filtered_articles.append({
                "title": title,
                "source": art.get('source').get('name'),
                "published": art.get('publishedAt'),
                "author": art.get('author')
            })

        if len(filtered_articles) == 50:
            break

    return filtered_articles
