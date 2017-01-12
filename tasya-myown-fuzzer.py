import subprocess
import requests
from random import seed, randint, random

count = 0
#Forever fuzzing
while True:
	bri_val = randint(0, 1000)
	x_val = randint(0,1000) * random()
	y_val = randint(0, 1000) * random()
	
	# print test case
	print "Fuzzing Test Case: " + str(count) + " bri: " + str(bri_val) + " x: " + str(x_val) + " y: " + str(y_val) 
	headers = {'Content-Type': 'application/json', 'X-Token': 'M0htalVOQTlFSldxWlYyMnJzbzVOeVFmdUFIWDRhL0N3REJyYXF3UFZqaz0='}
	data_1 = '{"on": "true", "bri": 123 ,"xy": [4.0, 4.0]}' # normal value
	data_2 = '{"on": "true", "bri":' + str(bri_val) + ', "xy": [' + str(x_val) + ',' + str(y_val) + ']}' # random value
	data_3 = '{"on": false}' # turn off value

	# PUT request, change data to desired set
	print(data_2)
	# r = requests.put('https://client.meethue.com/api/0/lights/1/state', data = data_2, headers = headers)
	r = requests.put('http://192.168.2.139/api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/1/state', data = data_2, headers = headers)
	print r.text
	count += 1