import subprocess
import requests
# This method is used to generate the fuzzing inputs to be used on the endpoint of the device. note that it can be customized based on a set of input list
def generate_hue_inputs():
    # this is to store the types of input that we will be fuzzing and generate variations of these inputs
    inputs_list = {"MAC Address":"01:02:03:04:05", "on": "False"}

    hue_inputs = {}
    # Generate all the possible random outputs for each possible input for philips HUE api endpoint to the bridge
    for key,value in inputs_list.iteritems():
        # Run radamsa fuzzer
        p1 = subprocess.Popen(["echo",inputs_list[key]],stdout= subprocess.PIPE)
        proc = subprocess.Popen(["radamsa","-n","1000"],stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close();
        (out, err) = proc.communicate()
        # Now we have a thousand fuzzed inputs to pump into the HUE to test.
        hue_inputs[key] = out.splitlines()
    return hue_inputs()
def send_hue_packet(url):
    requests.post(url,)

if __name__ == "__main__" :
    send_hue_packet()
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
