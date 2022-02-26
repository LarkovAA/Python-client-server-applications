from socket import *
import time
import json
import sys
from log_data import log_data
from common.additional_functions import checking_string_parameters, create_message
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
import logging
import log.client_log_config

@log_data
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

# server_connect = sys.argv
server_connect = ['', '127.0.0.1', 7777]
if __name__ == "__main__":
    logger = logging.getLogger('log_client')
    if len(server_connect) != 3 and len(server_connect) == 2:
        server_connect.append(SERVER_PORT)
    try:
        if checking_string_parameters(server_connect[1], server_connect[2]):
            logger.debug('Старт запросов пользователя')
            while True:
                client = socket(AF_INET, SOCK_STREAM)
                client.connect((str(server_connect[1]), int(server_connect[2])))
                presence_messege(client)

    except:
        logger.error(f'Клиент не смог зайти на сервер {server_connect[1]} орт {server_connect[2]}')