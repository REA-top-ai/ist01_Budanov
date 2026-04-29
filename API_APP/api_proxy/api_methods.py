import requests

BASE_URL = 'https://newsapi.org/v2'


def _make_requests(endpoint: str, api_key: str, params: dict[str, str] = None) -> dict[str, str]:
    url = f"{BASE_URL}/{endpoint}"
    # print(url)
    defalt_params = {'apiKey': api_key}

    if params:
        defalt_params.update(params)

    # print(defalt_params)
    try:
        response = requests.get(url, params=defalt_params, timeout=10)
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f'Ошибка в запросе к NewsAPI ({endpoint}): {e}')

    except ValueError as e:
        raise Exception(f"Ошибка типа JSON: {e}")


def get_top_headlines(api_key: str, q: str, country: str = None,
                      category: str = None, sources: str = None,
                      page_size: int = None) -> dict:

    allowed_params = {'q': q, 'country': country, 
                      'category': category, 'sources': sources,
                      'page_size': page_size}

    params = {key: value for key, value in allowed_params.items() if value is not None}

    return _make_requests('top-headlines', api_key, params)


def get_everything(api_key: str, q: str, search_in: str = None,
                   sources: str = None, domains: str = None,
                   exclude_domains: str = None, w_from: str = None,
                   to: str = None, language: str = None,
                   sort_by: str = None, page_size: int = None,
                   page: int = None) -> dict:

    allowed_params = {'q': q, 'searchIn': search_in,
                      'sources': sources, 'domains': domains,
                      'excludeDomains': exclude_domains, 'from': w_from,
                      'to': to, 'language': language, 'sortBy': sort_by,
                      'pageSize': page_size, 'page': page}

    params = {key: value for key, value in allowed_params.items() if value is not None}

    return _make_requests('everything', api_key, params)


def get_sources(api_key: str, category: str = None,
                language: str = None, country: str = None) -> dict:

    allowed_params = {'category': category,
                      'language': language, 'country': country}

    params = {key: value for key, value in allowed_params.items() if value is not None}

    return _make_requests('top-headlines/sources', api_key, params)

# Lm9Hwqybt4VIQLu9ouGHDuX1sChqx5Xc
