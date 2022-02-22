from socket import *
import json
import sys
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
from common.additional_functions import checking_string_parameters, checking_string, compose_answer


def run_server(MESSENGE_ENCODE, SERVER_PORT, server_connect):
    dict_client_register = {}
    dict_groupe = {}

    server_connect = server_connect
    if len(server_connect) != 5 and len(server_connect) == 3:
        server_connect.append('-p')
        server_connect.append(SERVER_PORT)

    if checking_string(server_connect):
        SERVER_IP = server_connect[server_connect.index('-a') + 1]
        SERVER_PORT = server_connect[server_connect.index('-p') + 1]
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((str(SERVER_IP), int(SERVER_PORT)))
        server.listen()

        while True:
            client, addr = server.accept()
            data = json.loads(client.recv(1024).decode(MESSENGE_ENCODE))
            if data['action'] == 'authenticate':
                if data['user']['account_name'] in dict_client_register.keys():
                    client.send(json.dumps(
                        compose_answer('authenticate', 'error', 101, 'Такой пользователь существует')).encode(
                        MESSENGE_ENCODE))
                else:
                    dict_client_register[data['user']['account_name']] = (data['user']['password'], client)
                    client.send(json.dumps(compose_answer('authenticate', 'alert', 202, 'Вы зарегистрированы')).encode(
                        MESSENGE_ENCODE))

            if data['action'] == 'presence':
                client.send(
                    json.dumps(compose_answer('presence', 'alert', 202, 'Вы подключены')).encode(MESSENGE_ENCODE))

            if data['action'] == 'msg':
                key_dict_client = dict_client_register.keys()

                if data['to'][0] != '#':
                    if data['to'] in key_dict_client:
                        client.send(json.dumps(compose_answer('msg', 'alert', 202, 'Ваше сообщение отправлено')).encode(
                            MESSENGE_ENCODE))
                    else:
                        client.send(json.dumps(compose_answer('msg', 'error', 404, 'Такого пользователя нет')).encode(
                            MESSENGE_ENCODE))
                else:
                    if data['to'][1:] in dict_groupe:
                        client.send(json.dumps(compose_answer('msg', 'alert', 202, 'Ваше сообщение отправлено')).encode(
                            MESSENGE_ENCODE))
                    else:
                        client.send(json.dumps(compose_answer('msg', 'error', 404, 'Такого группы нет')).encode(
                            MESSENGE_ENCODE))

            if data['action'] == 'quit':
                client.send(
                    json.dumps(compose_answer('quit', 'alert', 202, 'Вы вышли c сервера')).encode(MESSENGE_ENCODE))

            client.close()


if __name__ == '__main__':
    run_server(MESSENGE_ENCODE, SERVER_PORT, sys.argv)
