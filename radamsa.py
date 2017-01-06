import subprocess,json,requests,time,random,datetime,sys,ast

# This method is used to generate the fuzzing inputs to be used on the endpoint of the device. note that it can be customized based on a set of input list
def generate_hue_inputs(input_list):
    #  URL and token for local access
    # http: // 192.168.2.139/api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/1/state
    hue_inputs = {}
    # Generate all the possible random outputs for each possible input for philips HUE api endpoint to the bridge
    for key,value in input_list.iteritems():
        # Run radamsa fuzzer
        p1 = subprocess.Popen(["echo",str(input_list[key])],stdout= subprocess.PIPE)
        proc = subprocess.Popen(["radamsa"],stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close();
        (out, err) = proc.communicate()
        hue_inputs[key] = out
    return hue_inputs


def send_hue_packet(url,endpoint,option,inputs_list,timestamp,headers = {}):

    fuzz_data = generate_hue_inputs(inputs_list);
    all_log_file = open("fuzzlog_" + timestamp + ".txt", "a+")
    success_log_file = open("fuzzlog_success"+timestart +".txt", "a+")
    # Create a data packet to send to the hue api
    # light_no = random.randint(1,3)
    try:
        r = requests.put(url + endpoint + "1" + option, data=json.dumps(fuzz_data, ensure_ascii=False), headers=headers)
    except:
        all_log_file.write("{'url':\"" + url + endpoint + "1" + option + "\",'data': " + str(fuzz_data) + ",'headers':" + str(headers) + ", 'contents' : 'CONNECTION ERROR' }\n")
        return
    try:
        decoded_response = json.JSONDecoder().decode(r.text)
    except:
        all_log_file.write("{'url':\"" + url + endpoint + "1" + option + "\",'data': " + str(fuzz_data) + ",'headers':" + str(headers) + ", 'contents' : 'UNEXPECTED RESPONSE >> "+ r.text +"' }\n")
        return
    has_success = False
    for item in decoded_response:
        has_success = not 'error' in item
    if (r.status_code == 200 and has_success) or r.status_code != 200:
        write_format(success_log_file,url,endpoint,option,fuzz_data,headers)
        for item in r:
            for key,value in item:
                success_log_file.write(key + " : " + value + "\n")
    # Removed human readability from the log so I can easily parse the logfiles through Python to display
    all_log_file.write("{'url':\"" + url + endpoint + "1" + option + "\",'data': " + str(fuzz_data) + ",'headers':" + str(headers)+", 'contents' : " + r.content  + "}\n")


def write_format(file_input,url,endpoint,option,data,headers):
    file_input.write("\n-----------------NEW REQUEST----------------\n")
    file_input.write(url + endpoint + "1" + option + "\ndata = " + str(data) + "\nheaders = " + str(headers) + "\n")
    file_input.write("\n------------------RESPONSE------------------\n")


def generate_excel_format(timestamp):
    o = open("fuzzlog_excel"+timestamp+ ".txt","w+")
    logfile = open("fuzzlog_" + timestamp + ".txt", "r+")
    o.write("endpoint\tinput\tresult\tfull_contents\n")
    for line in logfile.readlines():
        decoded_line = ast.literal_eval(line)
        input_data = decoded_line['data']
        output_data = decoded_line['contents']
        # The order in which the input is given is the same order as the output data (ASSUMPTION FROM DATA COLLECTED, to make code more efficient)
        count = 0
        for key,value in input_data.iteritems():
            o.write(key+"\t"+repr(value)+"\t"+repr(output_data[count].keys()[0])+"\t"+str(output_data[count])+'\n')

    o.close()


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
    timestart = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m%-d%H%M%S')
    while(True):
        try:
            hue = random.randint(0, 65535)
            sat = random.randint(0, 255)
            bri = random.randint(0, 255)
            on = bool(random.getrandbits(1))
            inputs_list = {"bri": bri, "on": on, "hue": hue, "sat": sat}
            send_hue_packet('http://192.168.2.139/', 'api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/', '/state',inputs_list,timestart)
        except (KeyboardInterrupt, SystemExit):
            generate_excel_format(timestart)
            pass
