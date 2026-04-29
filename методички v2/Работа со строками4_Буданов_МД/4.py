def password_generator(first_name, last_name):
    return first_name[len(first_name)-3:] + last_name[len(last_name)-3:]

temp_password = password_generator('Петр','Андреев')
print(temp_password)