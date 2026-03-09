"""квадрат"""

def recursion_square(list, i=0, answers=[]):
    answers.append(list[i]**2)
    if i!=len(list)-1:
        return recursion_square(list, i+1, answers)
    else:
        return answers

print(recursion_square([3,4,5]))