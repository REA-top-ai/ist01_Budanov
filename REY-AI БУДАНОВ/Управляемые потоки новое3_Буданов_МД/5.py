statement_one = (2+2+2 >= 6) and (-1 * -1 > 0)
statement_two = (4 * 2 <= 8) and (7 - 1 == 6)
name = 'Dmitriy'
Dmitriy_arm = 122334
Angelina_arm = 12233
Vasiliy_arm = 12233
Ekaterina_arm = 1223
arm = 1223

if arm == Dmitriy_arm and name != 'Dmitriy':
    print('Добро пожаловать!')
elif arm == Dmitriy_arm and name == 'Dmitriy':
    print("Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!")
else:
    print('Логин или пароль не верный, попробуйте еще раз')

