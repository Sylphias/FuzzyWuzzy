import subprocess,json,requests,time,random

# This method is used to generate the fuzzing inputs to be used on the endpoint of the device. note that it can be customized based on a set of input list
def generate_hue_inputs(input_list):

    #  URL and token for local access
    # http: // 192.168.2.139/api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/1/state
    hue_inputs = {}
    # Generate all the possible random outputs for each possible input for philips HUE api endpoint to the bridge
    for key,value in inputs_list.iteritems():
        # Run radamsa fuzzer
        p1 = subprocess.Popen(["echo",str(inputs_list[key])],stdout= subprocess.PIPE)
        proc = subprocess.Popen(["radamsa"],stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close();
        (out, err) = proc.communicate()
        hue_inputs[key] = out
    return hue_inputs


def send_hue_packet(url,endpoint,option,inputs_list,headers = {}):
    fuzz_data = generate_hue_inputs(inputs_list);
    f = open("fuzzlog_all.txt", "a+")
    s = open("fuzzlog_success.txt", "a+")
    # Create a data packet to send to the hue api
    # light_no = random.randint(1,3)
    r = requests.put(url+endpoint+"1"+option, data=json.dumps(fuzz_data,ensure_ascii=False), headers=headers)
    decoded_response = json.JSONDecoder().decode(r.text)
    has_success = False
    for item in decoded_response:
        has_success = not 'error' in item
    if (r.status_code == 200 and has_success) or r.status_code != 200:
        write_format(s,url,endpoint,option,fuzz_data,headers)
        for item in r:
            for key,value in item:
                s.write(key + " : " + value + "\n")
    write_format(f, url, endpoint, option, fuzz_data, headers)
    f.write(str(r) + ' : ' + r.content + "\n");

# Keeping the code DRY
def write_format(file_input,url,endpoint,option,data,headers):
    file_input.write("\n-----------------NEW REQUEST----------------\n\n")
    file_input.write(url + endpoint + "1" + option + "\ndata = " + str(data) + "\nheaders = " + str(headers) + "\n")
    file_input.write("\n------------------RESPONSE------------------\n")


def party_lights():
    data = {}
    for count in range(0,1000):
        # Create a data packet to send to the hue api
        data["hue"] = random.randint(0, 65535)
        data["sat"] = random.randint(0, 255)
        data["on"] = True
        light_no = random.randint(1,3)
        r = requests.put('http://192.168.2.139/api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/'+str(light_no)+'/state', data=json.dumps(data))
        time.sleep(0.01)

# def verify_oracle(response):


if __name__ == "__main__" :
    # this is to store the types of input that we will be fuzzing and generate variations of these inputs
    while(True):
        try:
            hue = random.randint(0, 65535)
            sat = random.randint(0, 255)
            bri = random.randint(0, 255)
            on = bool(random.getrandbits(1))
            inputs_list = {"bri": bri, "on": on, "hue": hue, "sat": sat}
            send_hue_packet('http://192.168.2.139/', 'api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/', '/state',inputs_list)
        except KeyboardInterrupt:
            pass
    # party_lights()