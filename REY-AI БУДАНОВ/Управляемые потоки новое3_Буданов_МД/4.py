user_name = "Дмитрий"
Dmitriy_check = "Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!"
welcome_message = "Добро пожаловать"
enter_number = 3

if user_name == "Дмитрий":
    print(Dmitriy_check)
else:
    print(f"{welcome_message}, {user_name}!")

if enter_number < 3:
    print(f'Попробуйте еще раз. У вас осталось {enter_number} попыток')
else:
    print('Вы превысили максимальное кол-во попыток. Ваша учетная запись заблокирована.Для разблокировки обратитесь в службу поддержки')