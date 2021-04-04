#!/usr/bin/env python3

from _thread import *
import random
import time
import socket
import json
from flask import *
from threading import *

from time import sleep
from json import dumps
from kafka import KafkaProducer

from models import *

server_load = {}
apps_load = {}

with open('runtime_server.json') as f:
    server_list = json.loads(f.read())

app = Flask(__name__)
#app.config["DEBUG"] = True
producer = KafkaProducer(bootstrap_servers=[
                         'localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))


def init_servers():
    for x in server_list['servers']:
        #app = Flask(__name__)
        print(json.dumps(x))
        server_load[x['id']] = (
            Server(x['id'], x['ip'], x['port'], x['active'], x['health'], x['applications'],x['username'],x['password']))

        producer.send(KAFKA_TOPIC_SERVER_LIST, json.dumps(x))

        start_new_thread(app.run, (x['ip'], x['port'], True))
    input()


@app.route('/fetchDetails')
def fetchSensorData():
    if request.method == 'POST':
        return 'Not supported', 401
    x = request.args.get('id')
    if x is None:
        return {'msg': 'Server ID is absent'}, 400
    if int(x) not in server_load.keys():
        return {'msg': 'Server ID not found'}, 400
    sv = server_load[int(x)]
    return {'ip': sv.ip, 'port': sv.port, 'cpu': sv.cpu, 'ram': sv.ram, 'num_apps': sv.num_apps}, 200

@app.route('/runapp')
def runApplication():
    pass

# if __name__ == '__main__':
#     init_servers()
#     app.run(debug=True)
