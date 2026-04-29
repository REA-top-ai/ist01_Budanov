import random
name = input()
question = input()
answer = ''
random_number = random.randint(1, 9)
if random_number == 1:
    answer = 'Да, безусловно'
elif random_number == 2:
    answer = 'Совершенно верно'
elif random_number == 3:
    answer = 'Это решительно так'
elif random_number == 4:
    answer = 'Без сомнения'
elif random_number == 5:
    answer = 'Ответ туманный,попробуйте еще раз'
elif random_number == 6:
    answer = 'Спросите еще раз попозже'
elif random_number == 7:
    answer = 'Лучше не говорить вам сейчас'
elif random_number == 8:
    answer = 'Мои источники говорят нет'
elif random_number == 9:
    answer = 'Очень сомнительно'
else:
    print('Ошибка')
print(f'{name},спрашивает: {question}')
print(f'Магический шар отвечает: {answer}')