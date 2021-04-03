import _thread
import requests
import json
from kafka import KafkaConsumer

jobID = {}

def appExe(action, ID, appLoc, configLoc):
    global jobID

    if action == 'start':
        add = requests.get("localhost:4999/servermanager/assign_runtime_server/")
        add = add.json()
        ip = add["host"]
        port = add["port"]
        jobID[id] = [ip, port]
        #appServer("start", id, ip, port)
        #communicate with server passing action as an arg
    else:
        #communication with server using ip/port of jobID[id] along with action
        #appServer("end", id)
        pass
def main():
    
    consumer = KafkaConsumer('schedular',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        action = message.value["action"]
        ID = message.value["jobID"]
        appLoc = message.value["appLoc"]
        configLoc = message.value["configLoc"]
        _thread.start_new_thread(appExe,(action, ID, appLoc, configLoc,))

main()
