#!/usr/bin/env python3

from _thread import *
import random
import string
import time
import socket
import json
from flask import *
from threading import *
import requests

from time import sleep
from json import dumps
from kafka import KafkaProducer

from models import *

with open('runtime_server.json') as f:
    server_list = json.loads(f.read())

for i in range(0, len(server_list)):
    start_new_thread(startProbe, (i))

def startProbe(index):
	while True:
		x = server_list[index]
		ip = x['ip']
		port = x['port']
		r = requests.get(f'{ip}:{port}')
		if r.status_code == 200:
			print(f'Server {ip}:{port} is working normally')
		else:
			print(f'ERROR: Server {ip}:{port} is NOT responding')
		time.sleep(60)

input()