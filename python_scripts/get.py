import sys
import requests
import json

target = sys.argv[1]
config = requests.get('http://172.17.0.1:4999/config')
config = json.loads(config.text)
port = config[target]['port']

res = requests.get('http://172.17.0.1:'+str(port)+'/state')
print(res.text)
