import time
import sys
from commAPI import obj

class sensorapi(object):

    def __init__(self):
        self.sensor_count = int()
        self.controller_count = int()
        self.sensor = {"temp":"","ldr":""}
        self.controller = {"ac_controller":""}
        self.clocation = sys.argv[1]
    
    def setSensorCount(self, count):
        self.sensor_count = count

    def setControllerCount(self, count):
        self.controller_count = count

    def bindSensors(self):
        with open(self.clocation, "r") as f:
            data = json.loads(f.read())
            sinstances = data["sensors"]
            cinstances = data["controllers"] 
            for i in sinstances.keys():
                self.sensor[i] = sinstances[i]
            for i in cinstances.keys():
                self.controller[i] = cinstances[i]

    def getData(self, sensor):
        obj.getData("topic")

    def setData(self, controller, value):
        obj.setData("topic")
    def addSensorType(sensor):
        pass
    def removeSensorType(sensor):
        pass
    def addControllerType(sensor):
        pass
    def removeControllerType(sensor):
        pass
    def sendNotification():
        obj.sendNotification("topic")