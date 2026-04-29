import json
logs = [
    "2025-02-01 10:15:33|INFO|user=anna action=login status=success ip=10.0.0.1",
    "2025-02-01 10:17:10|ERROR|user=bob action=payment status=fail amount=120",
    "2025-02-01 10:20:01|INFO|user=anna action=logout status=success",
    "2025-02-01 10:22:45|WARNING|user=anna action=payment status=fail amount=300",
    "2025-02-01 10:30:12|ERROR|user=tom action=login status=fail ip=10.0.0.5"
]

# 1 задание

def log_conversion(line: str) -> dict:
    parts = line.split("|")
    date = parts[0] #хорошо бы проверять, что такой индекс есть в списке
    level = parts[1]
    message = parts[2]

    fields = message.split(" ")
    data = {}

    for f in fields:
        kv = f.split("=")
        if all(char.isdigit() for char in kv[1]):
            data[kv[0]] = int(kv[1])
        else:
            data[kv[0]] = kv[1]

    data["date"] = date #лучше через get()
    data["level"] = level
    return data

# 2 задание

def conversion_to_json(logs: list) -> list:
    parsed_logs = []
    for line in logs:
        parsed_logs.append(log_conversion(line))
    with open('logs_in_json.json', 'w') as file: json.dump(parsed_logs, file)
    return parsed_logs

parsed_logs = conversion_to_json(logs)

# 3 задание

def filter_logs(parsed_logs: list, **kwargs: str ) -> list:
    result = []
    for log in parsed_logs:
        for kwarg in kwargs:
            if (kwarg,kwargs[kwarg]) in log.items():
                flag = True
            else:
                flag = False
                break
        if flag:
            result.append(log)
    return result

# 4 задание

def count_by_level(parsed_logs: list)-> dict:
    count_level={}
    for log in parsed_logs:
        if log["level"] in count_level:
            count_level[log["level"]] += 1
        else:
            count_level[log["level"]] = 1
    return count_level

count_level_parsed_logs = count_by_level(parsed_logs)

def count_by_user(parsed_logs: list)-> dict:
    count_user={}
    for log in parsed_logs:
        if log["user"] in count_user:
            count_user[log["user"]] += 1
        else:
            count_user[log["user"]] = 1
    return count_user

count_user_parsed_logs = count_by_user(parsed_logs)

def sum_amount(parsed_logs: list)-> int:
    sum_amount=0
    for log in parsed_logs:
        if 'amount' in log:
            sum_amount += log["amount"]
    return sum_amount

sum_amount_parsed_logs = sum_amount(parsed_logs)

def count_by_action(parsed_logs: list)-> dict:
    count_action={}
    for log in parsed_logs:
        if log["action"] in count_action:
            count_action[log["action"]] += 1
        else:
            count_action[log["action"]] = 1
    return count_action

count_action_parsed_logs = count_by_action(parsed_logs)

def count_by_status(parsed_logs: list)-> dict:
    count_status={}
    for log in parsed_logs:
        if log["status"] in count_status:
            count_status[log["status"]] += 1
        else:
            count_status[log["status"]] = 1
    return count_status

count_status_parsed_logs = count_by_status(parsed_logs)

print("---- ONLY FAIL ONLY ----", *filter_logs(parsed_logs, status='fail'),sep='\n',end='\n\n')
print("---- ONLY ONLY ERRORS ----", *filter_logs(parsed_logs, level='ERROR'),sep='\n',end='\n\n')
print('---- ONLY ONLY ANNA ----', *filter_logs(parsed_logs, user='anna'),sep='\n',end='\n\n')

print(f'подсчет по level {count_level_parsed_logs}',end='\n\n')

print(f'подсчет по user {count_user_parsed_logs}',end='\n\n')

print(f'сумма amount = {sum_amount_parsed_logs}' ,end='\n\n')

print(f'подсчет по action {count_action_parsed_logs}',end='\n\n')

print(f'подсчет по status {count_status_parsed_logs}',end='\n\n')


