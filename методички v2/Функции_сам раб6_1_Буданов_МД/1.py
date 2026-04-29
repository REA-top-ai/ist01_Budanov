def f_to_c(f_temp):
    c_temp = (f_temp - 32) * 5/9
    return c_temp

f100_in_celsius = f_to_c(100)

def c_to_f(c_temp):
    f_temp = c_temp * 9 / 5 + 32
    return f_temp

c0_in_fahrenheit = c_to_f(0)
