from kafka import KafkaProducer
from kafka import KafkaConsumer
import time
import json

class comm(object):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        self.consumer1 = KafkaConsumer('sample',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        self.consumer2 = KafkaConsumer('sample',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))


    def getData(self, type, loc):
        
        data = {"msg":[type,loc]}
        self.producer.send('sample', value=data)
        time.sleep(0.009)

        for message in self.consumer1:
            message = message.value["data"]
            return message


    def setData(self, type, loc, value):

        data = {"msg":[type,loc,value]}
        self.producer.send('sample', value=data)
        time.sleep(0.009)

        for message in self.consumer2:
            message = message.value["data"]
            return message


    def sendNotification(self, msg):

        data = {"msg":msg}
        self.producer.send('sample', value=data)
        time.sleep(0.009)

obj = comm()
