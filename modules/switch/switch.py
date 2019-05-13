from flask import Flask, request, render_template
import requests
import argparse
import subprocess
import json
import os
import sys

if len(sys.argv) != 2:
    raise Exception('Invalid number of command line arguments. 1 expected, but ' + str(len(sys.argv) - 1) + ' given.\n')
target = sys.argv[1]
relayerPort = 4999

app = Flask(__name__)
@app.route('/', methods=['GET'])
def hello():
    return 'Hi, this switch is running.\n', 200

@app.route('/flip', methods=['POST'])
def flip():
    # Relayer url
    url = 'http://172.17.0.1:' + str(relayerPort) + '/send'

    # Action params
    NAMESPACE = 'guest'
    ACTION = 'flip_switch'

    data = {'namespace' : NAMESPACE,
            'action'    : ACTION,
            'ow_params'    : {
                'target': target
            }}

    response = requests.post(url, json=data)
    
    return 'Flip request sent to actuator ' + target + '.\n', 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
