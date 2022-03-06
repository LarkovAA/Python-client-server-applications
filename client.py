from socket import *
import time
import json
import sys
from log_data import log_data
from common.additional_functions import checking_string_parameters, create_message
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
import logging
import log.client_log_config
import threading

# @log_data
def presence_messege(client, name_client):
    msg_dict = {"action": "presence",
                "time": time.ctime(time.time()),
                "type": "status",
                "user": {"account_name": f"{name_client}",
                         "status": "Yep, I am here!"}
                }
    client.send(json.dumps(msg_dict).encode(MESSENGE_ENCODE))
    data = client.recv(1024)
    data = json.loads(data.decode(MESSENGE_ENCODE))
    logger.info(f'{data["alert"]}, код {data["response"]}')
    print(f'{data["alert"]}, код {data["response"]}')
    # client.close()
    # return data

# @log_data
def message(client,encoding, name_client):
    to = input('Введите имя кому хотите отправить сообщение. ')
    text = input('Введите текст сообщения: ')
    msg_dict = {
        "action": "msg",
        "time": time.ctime(time.time()),
        "encoding": encoding,
        "message": text,
        'from': name_client,
        'to': to
    }
    client.send(json.dumps(msg_dict).encode(encoding))
    # data = client.recv(1024)
    # data = json.loads(data.decode(MESSENGE_ENCODE))
    # print(data['alert'])
    # if data["response"] == 202:
    #     logger.info(f'{data["response"]} {data["alert"]}')
    #     print(f'{data["alert"]} {data["time"]}')
    # if data["response"] == 404:
    #     logger.info(f'{data["alert"]} {data["error"]}')
    #     print(f'{data["response"]} {data["error"]}')
    # client.close()
    # return data

def quit(client, encoding, name_client):
    global exit
    msg_dict = {
        "action": "quit",
        "user": {"account_name": f"{name_client}",
                 "status": "Yep, I am here!"}
        }
    client.send(json.dumps(msg_dict).encode(encoding))
    data = client.recv(1024)
    data = json.loads(data.decode(MESSENGE_ENCODE))
    logger.info(f'{data["response"]} {data["alert"]}')
    # print(f'{data["response"]} {data["alert"]}')
    time.sleep(0.5)
    exit = True
    client.close()
    # return data

def receive_data(client):
    data = client.recv(1024)
    data = json.loads(data.decode(MESSENGE_ENCODE))
    print(data['alert'], data['time'])

def the_main_process(client, MESSENGE_ENCODE):
    command = input('Введите команду ')
    if command == 'message':
        message(client, MESSENGE_ENCODE, name_client)
    if command == 'exit':
        quit(client, MESSENGE_ENCODE, name_client)

name_client = 'client1'
server_connect = ['', '127.0.0.1', 7777]
exit = False
client = None

if __name__ == "__main__":
    logger = logging.getLogger('log_client')
    if len(server_connect) != 3 and len(server_connect) == 2:
        server_connect.append(SERVER_PORT)
    try:
        if checking_string_parameters(server_connect[1], server_connect[2]):
            logger.debug('Старт запросов пользователя')
            client = socket(AF_INET, SOCK_STREAM)
            client.connect((str(server_connect[1]), int(server_connect[2])))
            presence_messege(client, name_client)
            print(f'Клиент: {name_client}\n Поддерживаемые команды:\n message - отправить сообшение. Кому и текст;\n exit - выйти из приложения. ')

            flow_1 = threading.Thread(target=receive_data, args=(client,))
            flow_2 = threading.Thread(target=the_main_process, args=(client, MESSENGE_ENCODE))
            flow_1.daemon = True
            flow_2.daemon = True
            flow_1.start()
            flow_2.start()

            while True:
                time.sleep(0.1)
                if exit:
                    break

    except:
        logger.error(f'Клиент не смог зайти на сервер {server_connect[1]} орт {server_connect[2]}')