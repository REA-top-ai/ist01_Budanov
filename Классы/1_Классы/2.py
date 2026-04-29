class Grade:
    minimum_passing = 65

class Rules:
    def washing_brushes(self):
        print('Point bristles towards the basin while washing your brushes.')
R = Rules()
print(R.washing_brushes())

class Circle():
    def __init__(self, diameter):
        self.radius = diameter/2
        print(f'New circle with diameter: {diameter}')
    def __repr__(self):
        return f'Circle with radius {self.radius}'
    pi = 3.14
    def area(self):
        area = self.pi * (self.radius) ** 2
        return area
    def circumference(self):
        circumference = 2 * self.pi * self.radius
        return circumference
medium_pizza = Circle(12)
teaching_table = Circle(36)
round_room = Circle(11460)

print(medium_pizza.circumference())
print(teaching_table.circumference())
print(round_room.circumference())

print(medium_pizza)
print(teaching_table)
print(round_room)
