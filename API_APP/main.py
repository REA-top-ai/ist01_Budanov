# import requests as r
# import pprint

# result = r.get('https://newsapi.org/v2/everything?
# apiKey=7a5108b3318e4ed2812a864f7e5f8355=bitcoin')
# pprint.pprint(result.json())

# from api_proxy import get_top_headlines
# from Api_analytics.analytycs import give_50_filtered_news
# import pprint

# if __name__ == '__main__':
#     result = get_top_headlines(q='apple',
#                                api_key='7a5108b3318e4ed2812a864f7e5f8355')
#     result1 = give_50_filtered_news(q='samsung',
#                                     api_key='7a5108b3318e4ed2812a864f7e5f8355')
#     pprint.pprint(result)
#     pprint.pprint(result1)

#   ВСЕ ЧТО ВЫШЕ БЫЛО СТО ЛЕТ НАЗАД

from mistral_request import post_annotation


if __name__ == '__main__':
    api_key_for_news = '7a5108b3318e4ed2812a864f7e5f8355'
    key_word = 'Apple'
    reports = post_annotation(key_word=key_word, api_key=api_key_for_news)
    with open('Result_of_ai_report.txt', 'w', encoding='utf-8') as f:
        f.write(reports)
