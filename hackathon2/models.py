#!/usr/bin/env python3


class Application:
    def __init__(self, app_id, user_id, sensor_list, ip, port, ram_req, cpu_req, app_path, algo_path):
        self.app_id = app_id
        self.user_id = user_id
        self.sensor_list = sensor_list
        self.ip = ip
        self.port = port
        self.ram_req = ram_req
        self.cpu_req = cpu_req
        self.app_path = app_path
        self.algo_path = algo_path


class Server:
    def __init__(self, id, ip, port, cpu, ram, num_apps):
        self.id = id
        self.ip = ip
        self.port = port
        self.cpu = cpu
        self.ram = ram
        self.num_apps = num_apps


KAFKA_TOPIC_SERVER_LIST = 'server_list'
