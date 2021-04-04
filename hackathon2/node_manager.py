#!/usr/bin/env python3

from _thread import *
import random
import string
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
apps_load = []
last_port = 0

with open('runtime_server.json') as f:
    server_list = json.loads(f.read())

app = Flask(__name__)
#app.config["DEBUG"] = True
producer = KafkaProducer(bootstrap_servers=[
    'localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))


def init_servers():
    for x in server_list:
        #app = Flask(__name__)
        # print(json.dumps(x))
        print(x['ip'], x['port'])
        server_load[x['id']] = (
            Server(x['id'], x['ip'], x['port'], x['active'], x['health'], x['applications'], x['username'], x['password']))
        last_port = x['port']
        producer.send(KAFKA_TOPIC_SERVER_LIST, json.dumps(x))

        start_new_thread(app.run, (x['ip'], x['port']))
    input()

def createNodeServer():
    global last_port
    ip = '127.0.0.1'
    l = len(server_load)
    last_port += 1
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    server_list.append({'id': id, 'ip': ip, 'port': last_port, 'active': 1,
                                            'health': 1, 'applications': 0, 'username': 'test', 'password': 'test'})
    server_load[id] = Server(id, ip, last_port, active=1, health=1,
                             applications=0, username='test', password='test')

    with open('runtime_server.json', 'w') as f:
        json.dump(server_list, f)

    producer.send(KAFKA_TOPIC_SERVER_LIST, json.dumps(x))
    #start_new_thread(app.run, (x['ip'], x['port'], True))


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


@app.route('/')
def checkServerHealth():
    if request.method == 'POST':
        return 'Not supported', 401
    return {'msg': 'Server health check successful'}, 200


@app.route('/runapp')
def runApplication():
    if request.method == 'POST':
        return 'Not supported', 401
    app_id = request.args.get('app_id')
    user_id = request.args.get('user_id')
    sensor_list = request.args.get('sensor_list')
    ram_req = request.args.get('ram_req')
    cpu_req = request.args.get('cpu_req')
    app_path = request.args.get('app_path')
    algo_path = request.args.get('algo_path')
    ip = request.host
    port = request.host
    if app_id is None:
        return {'msg': 'App ID is absent'}, 400
    if user_id is None:
        return {'msg': 'User ID is absent'}, 400
    if app_path is None:
        return {'msg': 'App Path is absent'}, 400
    if algo_path is None:
        return {'msg': 'Algo Path is absent'}, 400
    apps_load.append(Application(app_id, user_id, sensor_list,
                                 ip, port, ram_req, cpu_req, app_path, algo_path))
    return {'msg': 'Success'}, 200
    # execute APP


@app.route('/stopapp')
def stopApplication():
    if request.method == 'POST':
        return 'Not supported', 401
    app_id = request.args.get('app_id')
    user_id = request.args.get('user_id')
    if app_id is None:
        return {'msg': 'App ID is absent'}, 400
    if user_id is None:
        return {'msg': 'User ID is absent'}, 400
    for i in range(0, len(apps_load)):
        ap = apps_load[i]
        if ap.app_id == app_id and ap.user_id == user_id:
            apps_load.pop(i)
            return {'msg': 'Success'}, 200
    return {'msg': 'App ID not found'}, 401


init_servers()
# if __name__ == '__main__':
#     init_servers()
#     app.run(debug=True)
