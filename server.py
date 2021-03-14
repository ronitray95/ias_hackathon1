import pymongo as pm
from pymongo.encryption import Algorithm
#import communication 
from datetime import datetime
import json
import _thread
import requests
import time

def notify(instance):
    requests.post("localhost:8000/", json=json.dumps({"notification":"Eneven pulse detected, location:room1, xyz hospital"}))

def execute_algo(algo, type):
    
    high = algo['conditions']['pulse_rate'][0]
    low = algo['conditions']['pulse_rate'][1]
    while(1):
        data = requests.get('localhost:5000/')
        data = data.json()
        if data['low'] <= low or data['high'] >= high:
            if type == 'monitor':
                notify()
            else:
                perform_action()


def run_algo():
    #appID = instance['appID']
    appID = "app1"
    #sensorList = instance['sensor list']
    sensorList = ['s1','s2','s3']
    #application = db['application registration']
    #cu_app = application.find({'appID':appID})[0]
    #file_location = cu_app['location']
    file_location = '/app1/algorithm'
    with open(file_location) as f:
        algo = json.load(f)
    execute_algo(algo,'monitor')

def perform_action():
    pass

def main():
    client = pm.MongoClient("mongodb+srv://admin:admin123@cluster0.ze4na.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    #db = client("hackathon")
    #scheduler = db['schedule']
    sample = ['10:30','11:15','11:30']
    now = datetime.now()
    while True:
        time.sleep(60)
        current_time = '11:30'
        #instance = scheduler.find({'start_time':current_time})
        if current_time in sample:
            run_algo()        
        else:
            continue
        
main()