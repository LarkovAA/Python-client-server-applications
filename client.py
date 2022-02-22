from socket import *
import time
import json
import sys
from common.additional_functions import checking_string_parameters, create_message
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
import logging
import log.client_log_config


def presence_messege(client):
    msg_dict = {"action": "presence",
                "time": 10,
                #time.ctime(time.time())
                "type": "status",
                "user": {"account_name": "C0deMaver1ck",
                         "status": "Yep, I am here!"}
                }
    client.send(json.dumps(msg_dict).encode(MESSENGE_ENCODE))
    data = client.recv(1024)
    data = json.loads(data.decode(MESSENGE_ENCODE))
    logger.info(f'{data["alert"]}, код {data["response"]}')
    # print(f'{data["alert"]}, код {data["response"]}')
    client.close()
    return data

def message(client,encoding):
    msg_dict = {
        "action": "msg",
        "time": time.ctime(time.time()),
        "to": "server",
        "from": "C0deMaver1ck",
        "encoding": encoding,
        "message": 'Hello word'}
        #create_message()
    client.send(json.dumps(msg_dict).encode(encoding))
    data = client.recv(1024)
    data = json.loads(data.decode(MESSENGE_ENCODE))
    if data["response"] == 202:
        logger.info(f'{data["response"]} {data["alert"]}')
        # print(f'{data["response"]} {data["alert"]}')
    if data["response"] == 404:
        logger.info(f'{data["response"]} {data["error"]}')
        # print(f'{data["response"]} {data["error"]}')
    client.close()
    return data

def register_client(client, encoding):
    global registr_clients
    msg_dict = {
        "action": "authenticate",
        "time": time.ctime(time.time()),
        "user": {"account_name": "C0deMaver1ck",
                 "password":'CorrectHorseBatteryStaple'}}  #coding_password("CorrectHorseBatteryStaple") пытался закодировать пароль нельзя закодированное в base64 закодировать в utf
    client.send(json.dumps(msg_dict).encode(encoding))
    data = client.recv(1024)
    data = json.loads(data.decode(MESSENGE_ENCODE))
    if data["response"] == 202:
        logger.info(f'{data["response"]} {data["alert"]}')
        # print(f'{data["response"]} {data["alert"]}')
        registr_clients = True
    if data["response"] == 101:
        logger.info(f'{data["response"]} {data["error"]}')
        # print(f'{data["response"]} {data["error"]}')
    client.close()
    return data

def quit(client, encoding):
    global exit
    msg_dict = {
        "action": "quit",
        "user": {"account_name": "C0deMaver1ck",
                 "status": "Yep, I am here!"}
        }
    client.send(json.dumps(msg_dict).encode(encoding))
    data = client.recv(1024)
    data = json.loads(data.decode(MESSENGE_ENCODE))
    logger.info(f'{data["response"]} {data["alert"]}')
    # print(f'{data["response"]} {data["alert"]}')
    exit = True
    client.close()
    return data

exit = False
helps = 0
registr_clients = False
server_connect = sys.argv

dict_commands_client = {1: 'зарегистрироваться', 2: 'проверить подключение', 3: 'отправить сообщение', 4: 'выйти'}

if __name__ == "__main__":
    logger = logging.getLogger('log_client')

    if len(server_connect) != 3 and len(server_connect) == 2:
        server_connect.append(SERVER_PORT)
    try:
        if checking_string_parameters(server_connect[1], server_connect[2]):
            logger.debug('Старт запросов пользователя')
            while True:
                if helps != 1:
                    print('1-зарегистрироваться 2-проверить подключение 3-отправить сообщение 4-выйти')
                    helps += 1
                command = int(input())
                logger.debug(f'Клиент выбрал команду {dict_commands_client[command]}')
                if command == 1:
                    if registr_clients == False:
                        client = socket(AF_INET, SOCK_STREAM)
                        client.connect((str(server_connect[1]), int(server_connect[2])))
                        register_client(client, MESSENGE_ENCODE)
                    else:
                        logger.info('Вы уже зарегистрированы')
                        # print('Вы уже зарегистрированы')

                if command == 2:
                    client = socket(AF_INET, SOCK_STREAM)
                    client.connect((str(server_connect[1]), int(server_connect[2])))
                    presence_messege(client)

                if command == 3:
                    client = socket(AF_INET, SOCK_STREAM)
                    client.connect((str(server_connect[1]), int(server_connect[2])))
                    message(client, MESSENGE_ENCODE)

                if command == 4:
                    client = socket(AF_INET, SOCK_STREAM)
                    client.connect((str(server_connect[1]), int(server_connect[2])))
                    quit(client, MESSENGE_ENCODE)
                    if exit:
                        logger.debug('Пользователь вышел')
                        break
    except:
        logger.error(f'Клиент не смог зайти на сервер {server_connect[1]} орт {server_connect[2]}')