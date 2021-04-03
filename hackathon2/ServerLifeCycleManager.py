from flask import Flask,jsonify,request,Response,json
import threading

app = Flask(__name__)
app.config["DEBUG"] = True

""" 
@app.route("/",methods=['GET'])
def hello():
    return "Hello World!" """



def running_runtime(id):
    print(id)


@app.route("/servermanager/assign_runtime_server/<id>")
def allocate_server(id):
	myruntime_server=threading.Thread(target=running_runtime,args=(id,))
	myruntime_server.start()
	return_status={"server_allocation":"success"}
	server_allocation_status = Response(json.dumps(return_status), status=200, mimetype='application/json')
	return server_allocation_status


if __name__ == "__main__":
    app.run()