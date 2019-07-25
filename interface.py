#!/usr/bin/python3
from flask import Flask
from flask import request, jsonify
import json
import service as s

app = Flask(__name__)


@app.route('/requests', methods=['POST'])
def requestFor_Event_And_Txns():
    print("123456789")
    clientId = request.headers["clientId"]
    print("cid", clientId)
    data = request.data
    print("data: ", data)

    if data is None:
        file = request.files["file"]
        print("file", file)
        readFile = file.stream.read()
        inputCommand = request.form["command"]
        inputParams = request.form["params"]

        params = inputParams.split(",")
        params.append(readFile)
        inputData = {"command": inputCommand, "params": params}
    else:
        print("else")
        inputData = json.loads(data)
        print(inputData)
    output = s.parseData(inputData, clientId)
    result = json.dumps({"result": output})

    return result
