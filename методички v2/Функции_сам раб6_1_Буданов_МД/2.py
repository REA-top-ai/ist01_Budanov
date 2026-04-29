def get_force(weight,acceleration):
    return weight * acceleration

train_mass = 10
train_acceleration = 20
train_force = get_force(train_mass,train_acceleration)

print(train_force)
print(f'Поезд GE поставляет {train_force} ньютонов силы')

def get_energy(weight,c=3*10**8):
    return weight * c**2

bomb_energy = get_energy(1)
print(f'1 кг бомбы составляет {bomb_energy} Джоулей')

def get_work(weight,c,distance):
    strength = get_energy(weight,c)
    return strength * distance

train_mass = 22680
train_acceleration = 10
train_distance = 100
train_work = get_work(train_mass,train_acceleration,train_distance)

print(f'Поезд выполняет {train_work} Джоулей за {train_distance} метров.')