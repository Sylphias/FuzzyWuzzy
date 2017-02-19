import subprocess,json,requests,time,random,datetime,sys,ast,re, thread, threading, __future__


class RadamsaThread(threading.Thread):
    def __init__(self,number):
        threading.Thread.__init__(self)
        self.number = number

    def stop(self):
        self._Thread__stop()

    #There is a certain amout of time needed for radamsa to run and produce a full output. so dont set the timer to be too low.
    def run(self):
        threadlock = threading.Lock()
        threading.Timer(0.1,self.run).start()
        threadlock.acquire()
        hue = random.randint(0, 65535)
        sat = random.randint(0, 255)
        bri = random.randint(0, 255)
        on = bool(random.getrandbits(1))
        print("FuzzThread "+ str(self.number) + " Is Running")
        inputs_list = {"bri": bri, "on": on, "hue": hue, "sat": sat}
        sendFuzzPacketOnly('http://192.168.2.139/', 'api/zLcVDH439gTV3VGebD-s7XhS4DTvAAupN7VDGhIw/lights/', '/state',inputs_list)
        threadlock.release()

# This method is used to generate the fuzzing inputs to be used on the endpoint of the device. note that it can be customized based on a set of input list
def generate_hue_inputs(input_list):
    #  URL and token for local access
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
    outlier_log_file = open("fuzzlog_failures"+ timestamp +".txt", "a+")
    try:
        r = requests.put(url + endpoint + "1" + option, data=json.dumps(fuzz_data, ensure_ascii=False), headers=headers)
    except:
        connection_log = "{'url':\'" + url + endpoint + "1" + option + "\','data': " + str(fuzz_data) + ",'headers':" + str(headers) + ", 'contents' : CONNECTION ERROR >> "+ str(sys.exc_info()[0].message) +"}\n"
        all_log_file.write(connection_log)
        outlier_log_file.write(connection_log)
        return
    try:
        decoded_response = json.JSONDecoder().decode(r.text)
    except:
        all_log_file.write("{'url':\'" + url + endpoint + "1" + option + "\','data': " + str(fuzz_data) + ",'headers':" + str(headers) + ", 'contents' : UNEXPECTED RESPONSE: ERROR >> "+ str(sys.exc_info()[0].message)+" Contains >> "+ r.text +" }\n")
        return
    has_success = False
    for item in decoded_response:
        has_success = not 'error' in item
    if (r.status_code == 200 and has_success) or r.status_code != 200:
        write_format(outlier_log_file,url,endpoint,option,fuzz_data,headers)
        for item in r:
            for key,value in item:
                outlier_log_file.write(key + " : " + value + "\n")
    # Removed human readability from the log so I can easily parse the logfiles through Python to display
    all_log_file.write("{'url':\"" + url + endpoint + "1" + option + "\",'data': " + str(fuzz_data) + ",'headers':" + str(headers)+", 'contents' : " + r.content  + "}\n")

def sendFuzzPacketOnly(url,endpoint,option,inputs_list,headers = {}):
    fuzz_data = generate_hue_inputs(inputs_list);
    try:
        r = requests.put(url + endpoint + "1" + option, data=json.dumps(fuzz_data, ensure_ascii=False), headers=headers)
    except requests.exceptions.RequestException as e:
        print(e.message)



def spawn_multiple_instances(noOfThread):
    fuzz_threads =[]
    counter = 0
    for threads in range(noOfThread):
        fuzz_threads += [RadamsaThread(counter)]
        counter +=1
    for fuzzThread in fuzz_threads:
        fuzzThread.run()
    return fuzz_threads



def write_format(file_input,url,endpoint,option,data,headers):
    file_input.write("\n-----------------NEW REQUEST----------------\n")
    file_input.write(url + endpoint + "1" + option + "\ndata = " + str(data) + "\nheaders = " + str(headers) + "\n")
    file_input.write("\n------------------RESPONSE------------------\n")



def radamsa(options, payloadfile):
    file = open(payloadfile,"r")
    

if __name__ == "__main__" :
    # this is to store the types of input that we will be fuzzing and generate variations of these inputs
    timestart = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m%-d%H%M%S')
    fuzz_threads = spawn_multiple_instances(4)

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
            for fuzzThread in fuzz_threads:
                fuzzThread.stop()
            break

    # generate_excel_format("2017-028203243")