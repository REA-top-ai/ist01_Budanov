rate_movie = lambda rating: 'Мне понравился этот фильм' if rating>8.5 else 'Этот фильм был не очень хорошим'
print(rate_movie(8.6))
print(rate_movie(5))