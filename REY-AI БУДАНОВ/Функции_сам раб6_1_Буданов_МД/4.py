user_name = 'Дмитрий'
Dmitriy_check = 'Дмитрий, твое рабочее место находится в другой комнате.Отойди от чужого компьютера и займись работой!'
print('Добро пожаловать')

def check_name(user_name):
    if user_name == 'Дмитрий':
        return print(Dmitriy_check)
    else:
        return print('Добро пожаловать')

check_name(user_name)

Dmitriy_arm = 1231
Angelina_arm = 1232
Vasiliy_arm = 1233
Ekaterin_arm = 1234
arm = 1232

def check_arm_name(user_name,Arm):
    if user_name == 'Дмитрий' or arm == Dmitriy_arm:
        return print(Dmitriy_check)
    elif user_name != 'Дмитрий' and arm != Arm:
        print('Логин или пароль не верный, попробуйте еще раз')
    else:
        return print('Добро пожаловать')

check_arm_name(user_name,Angelina_arm)
