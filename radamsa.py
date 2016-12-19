import subprocess
def send_hue_packet():
    hue_http = "https://www.meethue.com/api/nupup"
    # this is to store the types of input that we will be fuzzing and generate variations of these inputs
    inputs_list = {}
    
    hue_inputs = {}
    # Generate all the possible rando
    for key,value in inputs_list.iteritems():
        proc = subprocess.Popen(["radamsa","-n 1000"],stdin=inputs_list[key], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()


if __name__ == "__main__" :
    while(True):
        try:
            send_hue_packet()
        except KeyboardInterrupt:
            pass



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
