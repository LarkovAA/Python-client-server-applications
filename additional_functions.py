def checking_numbers_func(checking_numbers:list):
    for num in checking_numbers:
        try:
            num = int(num)
        except:
            return True
    return False

def checking_string_parameters(server_ip:str, server_port=7777):
    number_points = server_ip.count('.')
    checking_numbers = server_ip.split('.')

    if number_points != 3 or checking_numbers_func(checking_numbers):
        raise ValueError('Введите правильное значение IP')
    try:
        server_port = int(server_port)
    except:
        raise ValueError('Введите правильное значение порта')

    if server_port < 1024:
        raise ValueError('Введите недопустипое значение порта. Данный порт уже зарезервирован.')
    if server_port > 65536:
        raise ValueError('Введите недопустипое значение порта. Данного порта не может сушествовать.')

    return True

def create_message(encoding):
    text = input('Введите сообщение: ')
    return text.encode(encoding)