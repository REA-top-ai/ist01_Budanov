"""Факториал"""
import time
import sys
sys.setrecursionlimit(10000)
a1=time.time()

def recursion_factory(n):
    if n==1:
        return 1
    else:
        return n*recursion_factory(n-1)

print(recursion_factory(100))

a2=time.time()

print(f'Время рекурсии: {a2-a1}')

# у рекурсионного метода изначально есть лимит рекурсии, поэтому его надо увеличивать, а для итеративного метода такого делать не надо



a3=time.time()

def iterative_factory(n):
    count=1
    while n>1:
        count*=n
        n-=1
    return count

print(iterative_factory(100))

a4=time.time()

print(f'Время итеративного метода: {a4-a3}')

# для 100 время работы одинаковое, но для больших данных
# для больших данных быстрее будет работать циклы??????????