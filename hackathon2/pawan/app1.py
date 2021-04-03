import API

min_threshold = 15
max_threshold = 28

api = API.sensorapi()
while(True):
    if api.getData("temp") < 15 or api.getData("temp") > 28:
        ack = api.setData("ac_controller", 20) 
        print("Temperture changed to {}".format(ack))
        #if ack == 1:
            #api.sendNotification("Temperature changed to 20")
