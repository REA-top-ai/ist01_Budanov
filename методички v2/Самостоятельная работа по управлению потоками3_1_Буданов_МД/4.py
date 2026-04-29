brand = "Volkswagen Polo"
age = 25
experience = 5
reputation = 2
traffic = 3
duration = 60

if brand == "Volkswagen Polo":
    if 20 <= age < 27 and 2 <= experience < 9 and 1 <= reputation <= 2 and 1 <= traffic <= 3:
        rate = 8
    elif 20 <= age < 27 and 2 <= experience < 9 and 1 <= reputation <= 2 and 4 <= traffic <= 7:
        rate = 8.5
    elif 20 <= age < 27 and 2 <= experience < 9 and 3 <= reputation <= 5 and 1 <= traffic <= 3:
        rate = 7.5
    elif 20 <= age < 27 and 2 <= experience < 9 and 3 <= reputation <= 5 and 4 <= traffic <= 7:
        rate = 7.4
    elif 27 <= age < 34 and 2 <= experience < 9 and 1 <= reputation <= 2 and 1 <= traffic <= 3:
        rate = 7.2
    elif 27 <= age < 34 and 2 <= experience < 9 and 3 <= reputation <= 5 and 1 <= traffic <= 3:
        rate = 7
    elif 27 <= age < 34 and 2 <= experience < 9 and 3 <= reputation <= 5 and 4 <= traffic <= 7:
        rate = 7.2
    elif 27 <= age < 34 and 10 <= experience < 15 and 1 <= reputation <= 2 and 1 <= traffic <= 3:
        rate = 6.9
    elif 27 <= age < 34 and 10 <= experience < 15 and 3 <= reputation <= 5 and 4 <= traffic <= 7:
        rate = 6.6
    elif 27 <= age < 34 and 10 <= experience < 15 and 1 <= reputation <= 2 and 4 <= traffic <= 7:
        rate = 6.7
    else:
        print("Для указанных параметров тариф не найден")
        rate = 0
elif brand == "BMW X1":
    if 20 <= age < 27 and 2 <= experience < 9 and 1 <= reputation <= 2 and 1 <= traffic <= 3:
        rate = 12
    elif 20 <= age < 27 and 2 <= experience < 9 and 1 <= reputation <= 2 and 4 <= traffic <= 7:
        rate = 12.5
    elif 20 <= age < 27 and 2 <= experience < 9 and 3 <= reputation <= 5 and 1 <= traffic <= 3:
        rate = 11.6
    elif 20 <= age < 27 and 2 <= experience < 9 and 3 <= reputation <= 5 and 4 <= traffic <= 7:
        rate = 11.3
    elif 27 <= age < 34 and 2 <= experience < 9 and 1 <= reputation <= 2 and 1 <= traffic <= 3:
        rate = 11.4
    elif 27 <= age < 34 and 2 <= experience < 9 and 3 <= reputation <= 5 and 1 <= traffic <= 3:
        rate = 11.7
    elif 27 <= age < 34 and 2 <= experience < 9 and 3 <= reputation <= 5 and 4 <= traffic <= 7:
        rate = 11.9
    elif 27 <= age < 34 and 10 <= experience < 15 and 1 <= reputation <= 2 and 1 <= traffic <= 3:
        rate = 10.8
    elif 27 <= age < 34 and 10 <= experience < 15 and 3 <= reputation <= 5 and 4 <= traffic <= 7:
        rate = 10.9
    elif 27 <= age < 34 and 10 <= experience < 15 and 1 <= reputation <= 2 and 4 <= traffic <= 7:
        rate = 11
    else:
        print("Для указанных параметров тариф не найден")
        rate = 0
else:
    print("Марка автомобиля не поддерживается")
    rate = 0

if rate > 0:
    price = rate * duration
    print(f"Стоимость вашей поездки составит {price}.")