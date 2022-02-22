import sys
sys.path.append('..')

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
        raise ValueError
        #('Введите недопустипое значение порта. Данного порта не может сушествовать.')

    return True

def create_message():
    text = input('Введите сообщение: ')
    return text

def checking_string(server_connect):
    if '-p' not in server_connect:
        raise ValueError('Введите корректно команду -p номер_порта')
    if '-a' not in server_connect:
        raise ValueError('Введите корректно команду -a ip_адресс')
    checking_string_parameters(server_connect[server_connect.index('-a')+1], server_connect[server_connect.index('-p')+1])
    return True

def compose_answer(action, code, response, text):
    if action in ['authenticate', 'presence', 'msg', 'quit'] and code == 'alert':
        answer_server = {
            'response': response,
            'alert': text,
            "time": 10 }
        # time.ctime(time.time())
        if action == 'presence':
            answer_server["action"] = "probe"
    if action in ['authenticate', 'presence', 'msg'] and code == 'error':
        answer_server = {
            'response': response,
            'error': text,
            "time": 10 }
        # time.ctime(time.time())
    return answer_server