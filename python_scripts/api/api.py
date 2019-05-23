from flask import Flask, request, render_template
import requests
import argparse
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/config', methods=['GET'])
def config():
    data = requests.get(url="http://172.17.0.1:4999/config").text
    return data

@app.route('/give_state', methods=['POST'])
def give_state():
    data = {}
    received_data = json.loads(request.data.decode('utf-8'))
    for key in received_data:
        if "a" in key:
            data[str(key)] = int(received_data[key]['state'])

    temp = requests.post(url="http://172.17.0.1:4000/", data=data)
    return "200"

@app.route('/get_state', methods=['GET'])
def get_state():
    result = requests.get(url='http://172.17.0.1:4000/state')
    return result.text

@app.route('/', methods=['POST'])
def node_1():
    # post data to switch
    url = 'http://172.17.0.1:' + request.form['port_number'] + '/flip'
    result = requests.post(url=url)

    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4001')
