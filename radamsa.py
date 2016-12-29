import subprocess,json,requests,time,random
# This method is used to generate the fuzzing inputs to be used on the endpoint of the device. note that it can be customized based on a set of input list
def generate_hue_inputs():
    # this is to store the types of input that we will be fuzzing and generate variations of these inputs
    inputs_list = {"bri":"123", "on": "True","hue":"12223", "sat":"123"}
    #  URL and token for local access
    # http: // 192.168.2.139/api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/1/state
    hue_inputs = {}
    # Generate all the possible random outputs for each possible input for philips HUE api endpoint to the bridge
    for key,value in inputs_list.iteritems():
        # Run radamsa fuzzer
        p1 = subprocess.Popen(["echo",str(inputs_list[key])],stdout= subprocess.PIPE)
        proc = subprocess.Popen(["radamsa","-n","1000"],stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close();
        (out, err) = proc.communicate()
        # Now we have a thousand fuzzed inputs to pump into the HUE to test.
        hue_inputs[key] = out.splitlines()
    return hue_inputs


def send_hue_packet(url,endpoint,option):
    fuzz_data = generate_hue_inputs();
    f = open("fuzzlog.txt", "a+")
    headers = {'Content-Type': 'application/json',
               'X-Token': 'M0htalVOQTlFSldxWlYyMnJzbzVOeVFmdUFIWDRhL0N3REJyYXF3UFZqaz0='}
    data = {}
    for count in range(0,1000):
        # Create a data packet to send to the hue api
        light_no = random.randint(1,3)
        for keys in fuzz_data.keys():
            data[keys] = fuzz_data[keys][count]
        r = requests.put(url+endpoint+str(light_no)+option, data=data, headers=headers)
        f.write("\n-----------------NEW REQUEST----------------\n\n")
        f.write(url+endpoint+str(light_no)+option + "\ndata = " + str(data) + "\nheaders = " + str(headers) + "\n")
        f.write("\n-----------------RESPONSE----------------\n")
        if type(r) is list:
            for item in r:
                for key,value in item:
                    f.write(key + " : " + value + "\n")
        else:
            f.write(str(r) + ' : ' + r.content + "\n");
        time.sleep(2)

def party_lights():
    # headers = {'Content-Type': 'application/json'}
    data = {}
    for count in range(0,1000):
        # Create a data packet to send to the hue api
        data["hue"] = random.randint(0, 65535)
        data["sat"] = random.randint(0, 255)
        light_no = random.randint(1,3)
        r = requests.put('http://192.168.2.139/api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/'+str(light_no)+'/state', data=json.dumps(data))
        time.sleep(0.01)

# def verify_oracle(response):


if __name__ == "__main__" :
    send_hue_packet('https://client.meethue.com/','api/0/lights/','/state')

    # party_lights()
    # while(True):
    #     try:
    #         send_hue_packet()
    #     except KeyboardInterrupt:
    #         pass



# import subprocess
#
# proc = subprocess.Popen(["radamsa", ])
# (out, err) = proc.communicate()
# print "program output:", out
#
# p1 = Popen(["dmesg"], stdout=PIPE)
# p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
# p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
# output = p2.communicate()[0]
#
# # Authentication request setup
#         data = {'grant_type': 'client_credentials'}
#         headers = {                                                   \
#                 'content-type' : 'application/x-www-form-urlencoded', \
#                 'Authorization': 'Basic ' + encodedSecurityInfo       \
#                 }
#
#         # Request authentication
#         data = urllib.urlencode(data)
#         request = urllib2.Request(config.auth_url, data, headers)
#         response = json.loads(urllib2.urlopen(request).read())
