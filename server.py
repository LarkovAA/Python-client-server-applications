from socket import *
import json
import time
import ast
import sys
from configurable_variables import MESSENGE_ENCODE, SERVER_PORT
from additional_functions import checking_string_parameters

server_connect = sys.argv
if len(server_connect) != 5 and len(server_connect) == 3:
    server_connect.append('-p')
    server_connect.append(SERVER_PORT)

def checking_string():
    if '-p' not in server_connect:
        raise ValueError('Введите корректно команду -p номер_порта')
    if '-a' not in server_connect:
        raise ValueError('Введите корректно команду -a ip_адресс')
    checking_string_parameters(server_connect[server_connect.index('-a')+1], server_connect[server_connect.index('-p')+1])
    return True

if checking_string():
    SERVER_IP = server_connect[server_connect.index('-a')+1]
    SERVER_PORT = server_connect[server_connect.index('-p')+1] if server_connect[server_connect.index('-p')+1] != False else SERVER_PORT
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((str(SERVER_IP), int(SERVER_PORT)))
    server.listen()

    while True:
        client, addr = server.accept()
        data = ast.literal_eval(client.recv(1024).decode(MESSENGE_ENCODE))
        if data['action'] == 'presence':
            answer_server = {
            'response': 202,
            'alert': 'Вы подключены',
            "action": "probe",
            "time": time.ctime(time.time())}
            client.send(json.dumps(answer_server).encode(MESSENGE_ENCODE))
            client.close()
        if data['action'] == 'msg':
            answer_server = {
            'response': 202,
            'alert': 'Ваше сообщение отправлено',
            "time": time.ctime(time.time())}
            client.send(json.dumps(answer_server).encode(MESSENGE_ENCODE))
            client.close()
