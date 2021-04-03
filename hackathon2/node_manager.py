#!/usr/bin/env python3

from _thread import *
import random
import time
import socket
import json
from flask import *
from threading import *

from models import *

server_load = {}

with open('server_details.json') as f:
    server_list = json.loads(f.read())

app = Flask(__name__)


def init_servers():
    for x in server_list:
        #app = Flask(__name__)
        server_load[int(x['id'])] = (
            Server(x['id'], x['ip'], x['port'], x['cpu'], x['ram'], 0))
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



if __name__ == '__main__':
    init_servers()
    # app.run(debug=True)
