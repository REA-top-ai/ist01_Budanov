def get_boundaries(target,margin):
    low_limit = target - margin
    hight_limit = target+margin
    return low_limit, hight_limit
print(get_boundaries(100,20))