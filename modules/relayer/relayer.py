from flask import Flask, request
import requests
import json
import sys

# if len(sys.argv) > 2:
#     raise Exception('Invalid number of command line arguments. 1 or less expected, but ' + str(len(sys.argv) - 1) + ' given.\n')

config = {}
if len(sys.argv) > 1:
    hostCount = int(sys.argv[1])
    print(hostCount)

    # generate config 
    config['r0'] = {
    'port': 4999,
    'docker_image': 'serverlessnet/relayer',
    'incoming': ['sw' + str(i) for i in range(hostCount)],
    'outgoing': ['a' + str(i) for i in range(hostCount)],
    'state': 'undefined'
    }
    for i in range(hostCount):
        config['sw' + str(i)] = {
            'port': (5000 + i),
            'docker_image': 'serverlessnet/switch',
            'incoming': [],
            'outgoing': [('a' + str(i))],
            'state': 'undefined'
        }
        config['a' + str(i)] = {
            'port': (5000 + hostCount + i),
            'docker_image': 'serverlessnet/actuator',
            'incoming': [('sw' + str(i))],
            'outgoing': [],
            'state': 0
        }

print(config)

baseUrl = 'http://172.17.0.1' # will need to automate this
apiPort = 4001

app = Flask(__name__)
@app.route('/', methods=['GET'])
def hello():
    # Status check
    return 'Hi, this relayer is running.\n', 200

@app.route('/config', methods=['GET'])
def getConfig():
    return json.dumps(config), 200

@app.route('/send', methods=['POST'])
def send():
    # Parse POST data
    data = json.loads(request.data.decode('utf-8'))
    ow_params = data['ow_params']
    # print('Data received: ')
    # print(data)

    '''
    DONT Cast target value to port number
    '''
    # ow_params['target'] = config[ow_params['target']]['port']

    # OpenWhisk setup
    # APIHOST = subprocess.check_output('wsk -i property get --apihost', shell=True).split()[3].decode('utf-8') 
    # AUTH_KEY = subprocess.check_output('wsk -i property get --auth', shell=True).split()[2].decode('utf-8')
    APIHOST = '192.168.1.202'
    AUTH_KEY = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP' 
    user_pass = AUTH_KEY.split(':')
    
    # In an ideal case, namespace and action should be parsed from requests from switch
    NAMESPACE = 'guest'
    ACTION = 'flip_switch'
    # NAMESPACE = data['namespace']
    # ACTION = data['action']

    # Construct trigger url
    url = 'http://' + APIHOST + ':8888' + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION

    # Some params
    PARAMS = ow_params
    BLOCKING = 'true'
    RESULT = 'true'

    # print(APIHOST)
    # print(AUTH_KEY)
    # Send post request
    response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))
    # print(response.text)
    
    return response.text

@app.route('/test', methods=['POST'])
def test():
    # APIHOST = subprocess.check_output('wsk -i property get --apihost', shell=True).split()[3].decode('utf-8') 
    # AUTH_KEY = subprocess.check_output('wsk -i property get --auth', shell=True).split()[2].decode('utf-8') 
    APIHOST = '192.168.1.202'
    AUTH_KEY = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
    NAMESPACE = 'guest'
    ACTION = 'hello_world'
    PARAMS = {'name':'Jerry'}
    BLOCKING = 'true'
    RESULT = 'true'

    print(APIHOST)
    print(AUTH_KEY)
    url = 'http://' + APIHOST + ':8888' + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION
    user_pass = AUTH_KEY.split(':')
    response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))
    print(response.text)
    
    return response.text

@app.route('/relay', methods=['POST'])
def relay():
    # Receive request from OpenWhisk
    data = json.loads(request.data.decode('utf-8'))
    targetHost = str(data['target'])
    actuatorUrl = str(data['url'])
    colon_idx = actuatorUrl.index(':', 5) # skip 'http://'
    actuatorUrl = actuatorUrl[:(colon_idx + 1)] + str(config[targetHost]['port']) + actuatorUrl[(colon_idx + 1):]

    print(actuatorUrl)
    
    apiURL = baseUrl + ':' + str(apiPort) + '/give_state'

    # Forward action to actuator
    a_res = requests.post(url=actuatorUrl)

    print(a_res.text)

    # update config
    config[targetHost]['state'] = int(json.loads(a_res.text)['state'])

    print(config)

    # Send the update to UI API
    api_res = requests.post(apiURL, json=config)

    return api_res.text, 200
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
