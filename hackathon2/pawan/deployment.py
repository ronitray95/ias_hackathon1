import _thread
import requests
import json
from kafka import KafkaConsumer

jobID = {}

def appExe(action, jID, aID, uID, RAM, CPU, appPath, algoPath, configPath):
    global jobID

    if action == 'start':
        ip =""
        port = ""
        consumer = KafkaConsumer('node-server-assign',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for message in consumer:
            ip = message.value["host"]
            port = message.value["port"]
            break 
        
        jobID[jID] = [ip, port]
        status = requests.get(ip+':'+port+'/runapp', params={'app_id': aID, 'user_id':uID, 'ram_req':RAM, 'cpu_req':CPU, 'app_path':appPath, 'algo_path':algoPath, 'config_path':configPath})
        if status:
            #return status to schedular
            pass

    else:
        status = requests.get(jobID[jID][0]+':'+jobID[jID][1]+'/stopapp', params={'app_id': aID, 'user_id':uID})
        if status:
            del jobID[jID]
def main():
    
    consumer = KafkaConsumer('schedular',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        action = message.value["action"]
        jID = message.value["jID"]
        appPath = message.value["appPath"]
        configPath = message.value["configPath"]
        uID = message.value["uID"]
        aID = message.value["aID"]
        RAM = message.value["RAM"]
        CPU = message.value["CPU"]
        algoPath =message.value["algoPath"]
        _thread.start_new_thread(appExe,(action, jID, aID, uID, RAM, CPU, appPath, algoPath, configPath))

main()
