import sys
import requests
import json
# get switch
sw = sys.argv[1]

config = requests.get("http://172.17.0.1:4999/config")
#print(config.text)
config = json.loads(config.text)

targetPort = config[sw]['port']
#print(targetPort)

res = requests.post('http://172.17.0.1:'+str(targetPort)+'/flip')
print(res.text)
