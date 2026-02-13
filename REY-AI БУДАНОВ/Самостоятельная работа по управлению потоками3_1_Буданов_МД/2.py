max_value = 25
mean_value = 10
min_value = 2
std_value = 3

if (max_value > mean_value + 5 * std_value) or (min_value < mean_value - 5 * std_value):
    print("В ваших данных имеются экстремальные значения и требуют предобработки")
elif (max_value > mean_value + 3 * std_value) or (min_value < mean_value - 3 * std_value):
    print("В ваших данных имеются выбросы и требуют предобработки")
else:
    print("Ваши данные пригодны для анализа")