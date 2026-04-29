def grade_test(rezult_test):
    if rezult_test >= 4.0:
        return 'A'
    elif rezult_test >= 3.0:
        return 'B'
    elif rezult_test >= 2.0:
        return 'C'
    elif rezult_test >= 1.0:
        return 'D'
    elif rezult_test >= 0.0:
        return 'F'

print(grade_test(4.1))
