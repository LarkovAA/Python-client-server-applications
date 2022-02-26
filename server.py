from socket import *
import json
import sys

from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
from common.additional_functions import checking_string_parameters, checking_string, compose_answer
import logging
import log.server_log_config

logger_server = logging.getLogger('log_server')


def run_server(MESSENGE_ENCODE, SERVER_PORT, server_connect):
    dict_client_register = {}
    dict_groupe = {}

    server_connect = server_connect
    if len(server_connect) != 5 and len(server_connect) == 3:
        server_connect.append('-p')
        server_connect.append(SERVER_PORT)
    # try:
    if checking_string(server_connect):
        SERVER_IP = server_connect[server_connect.index('-a') + 1]
        SERVER_PORT = server_connect[server_connect.index('-p') + 1]
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((str(SERVER_IP), int(SERVER_PORT)))
        server.listen()
        logger_server.debug('Создан сокет сервера. Начало работы.')
        while True:
            client, addr = server.accept()
            data = json.loads(client.recv(1024).decode(MESSENGE_ENCODE))
            if data['action'] == 'presence':
                client.send(
                    json.dumps(compose_answer('presence', 'alert', 202, 'Вы подключены')).encode(MESSENGE_ENCODE))
                logger_server.debug(f'Выполнен запрос на подключению сервера пользователя {data["user"]["account_name"]}')
            client.close()
    # except:
    #     logger_server.critical('Не правильно настроен сервер')

if __name__ == '__main__':
    run_server(MESSENGE_ENCODE, SERVER_PORT, ['', '-a', '127.0.0.1', '-p', 7777])
