single_digits = [digit for digit in range(10)]
squares = []

for digit in single_digits:
    print(digit)
    squares.append(digit**2)
print(squares)
cubes = [digit**3 for digit in single_digits]
print(cubes)

