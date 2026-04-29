def get_boundaries(target,margin):
    low_limit = target - margin
    high_limit = target + margin
    return low_limit,high_limit

low_limit,high_limit = get_boundaries(100,20)
print(f'Нижний предел:{low_limit},верхний предел:{high_limit}')