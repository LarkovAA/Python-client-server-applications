import select
from socket import *
import json
import sys
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
from common.additional_functions import checking_string_parameters, checking_string, compose_answer
import logging
import log.server_log_config

logger_server = logging.getLogger('log_server')

def run_server(MESSENGE_ENCODE, SERVER_PORT, server_connect):
    list_client_register = []
    dict_connected_clients = {}
    dict_groupe = {}

    server_connect = server_connect
    if len(server_connect) != 5 and len(server_connect) == 3:
        server_connect.append('-p')
        server_connect.append(SERVER_PORT)
    # try:
    if checking_string(server_connect):

        SERVER_IP = server_connect[server_connect.index('-a') + 1]
        SERVER_PORT = server_connect[server_connect.index('-p') + 1]

        with socket(AF_INET, SOCK_STREAM) as server:
            server.bind((str(SERVER_IP), int(SERVER_PORT)))
            server.listen()
            server.settimeout(1)

            logger_server.debug('Создан сокет сервера. Начало работы.')
            while True:
                try:
                    client, addr = server.accept()
                except OSError:
                    pass
                else:
                    list_client_register.append(client)
                finally:
                    time = 0
                    list_reader = []
                    list_write = []
                    list_error = []
                    try:
                        list_reader, list_write, list_error = select.select(list_client_register, list_client_register, [], time)
                    except Exception :
                        pass
                    try:
                        # print(list_write)
                        # print(list_reader)
                        for list_reader_client in list_reader:
                            data = json.loads(list_reader_client.recv(1024).decode(MESSENGE_ENCODE))
                            if data['action'] == 'presence':
                                try:
                                    for list_write_client in list_write:
                                        if list_reader_client == list_write_client:
                                            list_reader_client.send(
                                                json.dumps(compose_answer('presence', 'alert', 202,
                                                                          'Вы подключены')).encode(MESSENGE_ENCODE))
                                            logger_server.debug(
                                                f'Выполнен запрос на подключению сервера пользователя {data["user"]["account_name"]}')
                                            # list_client_register.remove(list_reader_client)
                                            dict_connected_clients[data['user']['account_name']] = list_reader_client
                                except:
                                    pass

                            if data['action'] == 'msg':
                                text = f"{data['message']} от {data['from']}"
                                to = data['to']
                                try:
                                    client = dict_connected_clients[to]
                                    client.send(json.dumps(compose_answer('msg', 'alert', 202, text)).encode(MESSENGE_ENCODE))
                                    # logger_server.debug(f'Выполнен отправка сообщения юзера: {data["from"]} к {to}')
                                    # list_reader_client.send(compose_answer('msg', 'alert', 202, 'Сообщение отправлено').encode(MESSENGE_ENCODE))
                                    # list_client_register.remove(list_reader_client)

                                    # for list_write_client in list_write:
                                    #     list_write_client.send(
                                    #         json.dumps(compose_answer('msg', 'alert', 202, text)).encode(
                                    #             MESSENGE_ENCODE))
                                    #     logger_server.debug(
                                    #         f'Выполнен отправка сообщения юзера: {data["user"]["account_name"]}')
                                    #     list_client_register.remove(list_write_client)
                                except:
                                    pass
                            if data['action'] == 'quit':
                                list_write_client.send(json.dumps(compose_answer('quit', 'alert', 202, 'Вы вышли')).encode(MESSENGE_ENCODE))
                                logger_server.debug(f'Выполнен выход юзера: {data["user"]["account_name"]}')
                                list_client_register.remove(list_reader_client)
                    except:
                        logger_server.debug(
                            f'Юзер: {data["user"]["account_name"]} вышел из чата')
                        list_client_register.remove(list_reader_client)
    # except:
    #     logger_server.critical('Не правильно настроен сервер')

if __name__ == '__main__':
    run_server(MESSENGE_ENCODE, SERVER_PORT, ['', '-a', '127.0.0.1', '-p', 7777])
