from abc import ABC, abstractmethod

print('=== СОТРУДНИКИ ===')

class AbstractEmployee:
    new_id = 1
    _id =100
    __id=123
    def __init__(self):
        self.id = Employee.new_id
        Employee.new_id += 1
        self._name = None

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        if isinstance(new_name, str):
            self._name = new_name

    def del_name(self):
        del self._name



    @abstractmethod
    def say_id(self):
        pass
print(dir(AbstractEmployee))
class Employee(AbstractEmployee):

    def say_id(self):
        print(f'My id is {self.id}')


e1 = Employee()
e2 = Employee()
e1.say_id()
e2.say_id()


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def say_user_info(self):
        print(f'My username is {self.username}')

print("=== АДМИН ===")
class Admin(Employee, User):
    def __init__(self):
        super().__init__()
        User.__init__(self, self.id, "Admin")
    def say_id(self):
        super().say_id()
        print('I am a Admin')
        return 'I am a Admin'
e3 = Admin()
e3.say_user_info()
e3.say_id()


print('=== МЕНЕДЖЕР ===')
class Manager(Admin):
    def say_id(self):
        super().say_id()
        print('I am a Manager')
        return 'I am a Manager'
e4 = Manager()
e4.say_id()

print("=== ВСТРЕЧА ===")
meeting = [e1, e3, e4]
for e in meeting:
    e.say_id()


print('=== ДОБАВЛЕНИЕ К ВСТРЕЧЕ ===')
class Meeting:
    def __init__(self, attendees):
        Meeting.attendees = attendees
    def __add__(self, other):
        for i in other:
            Meeting.attendees.append(i)
            print('Добавление к встрече!!!')
            i.say_id()
    def __len__(self):
        return len(Meeting.attendees)
m1 = Meeting([])
m1.__add__([e1])
m1.__add__([e2])
m1.__add__([e3])
print(f'На встече {m1.__len__()} человека')

print('=== ГЕТТЕРЫ, СЕТТЕРЫ, ДЕЛИТЕРЫ ===')
print(e1.get_name())
print(e1.set_name('sema'))
print(e1.get_name())
print(e1.del_name())





