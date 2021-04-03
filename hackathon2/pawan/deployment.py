import _thread
#import loadBalancer
#import appServer

jobID = {}

def appExe(data_from_schedular):
    global jobID
    data = json.loads(data_from_schedular)
    id = data["id"]
    action = data["action"]    
    if action == 'start':
        #ip, port = loadBalancer.getServer()
        #get ip, port here
        jobID[id] = [ip, port]
        #appServer("start", id, ip, port)
        #communicate with server passing action as an arg
    else:
        #communication with server using ip/port of jobID[id] along with action
        #appServer("end", id)
        pass
def main():
    #loop
    #read from schedular continuosly
    _thread.start_new_thread(appExe,(data_from_schedular,))
    
appExe(data_from_schedular)