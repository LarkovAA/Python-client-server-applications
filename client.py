import ast
from socket import *
import time
import json
import sys

from additional_functions import checking_string_parameters, create_message
from configurable_variables import MESSENGE_ENCODE, SERVER_PORT

def presence_messege(client):
    msg_dict = {"action": "presence",
                "time": time.ctime(time.time()),
                "type": "status",
                "user": {"account_name": "C0deMaver1ck",
                         "status": "Yep, I am here!"}
                }
    client.send(json.dumps(msg_dict).encode(MESSENGE_ENCODE))
    data = ast.literal_eval(client.recv(1024).decode(MESSENGE_ENCODE))
    print(f'{data["alert"]}, код {data["response"]}')
    client.close()

def message(encoding, client):
    msg_dict = {
        "action": "msg",
        "time": time.ctime(time.time()),
        "to": "C0deMaver1ck",
        "from": "server",
        "encoding": encoding,
        "message": create_message(encoding)}
    client.send(json.dumps(msg_dict).encode(encoding))
    data = json.loads(client.recv(1024).decode(MESSENGE_ENCODE))
    print(data)
    client.close()

server_connect = sys.argv
if len(server_connect) != 3 and len(server_connect) == 2:
    server_connect.append(SERVER_PORT)
if checking_string_parameters(server_connect[1], server_connect[2]):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((str(server_connect[1]), int(server_connect[2])))
    presence_messege(client)






