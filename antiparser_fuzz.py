from antiparser import *
import subprocess,json,requests,time,random,datetime,sys,ast,re, _thread, threading, __future__

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
    hue_inputs = {}
    for key,value in input_list.items():
        if type(value) == bool:
            hue_inputs[key] = []
            for x in range(100):
                hue_inputs[key].append(bool(random.getrandbits(1)))
            continue
        ap = antiparser()
        ap.setDebug(False)
        for x in range(100):
            newdata = apShort() # generate short inputs
            newdata.setMaxSize(65535) if key == "hue" else newdata.setMaxSize(255)
            ap.append(newdata)
        ap.permute()
        hue_inputs[key] = []
        for items in ap.getList():
            hue_inputs[key].append(items.content)
    return hue_inputs


def send_hue_packet(url,endpoint,option,input_list,timestamp,headers = {}):
    fuzz_data = generate_hue_inputs(input_list);
    all_log_file = open("fuzzlog_" + timestamp + ".txt", "a+")
    outlier_log_file = open("fuzzlog_failures"+ timestamp +".txt", "a+")
    # Create a data packet to send to the hue api
    # light_no = random.randint(1,3)
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



def generate_excel_format(timestamp):
    try:
        o = open("fuzzlog_excel"+timestamp+ ".txt","w+")
        logfile = open("fuzzlog_" + timestamp + ".txt", "r+")
        o.write("endpoint\tinput\tresult\tfull_contents\n")
        for line in logfile.readlines():
            try:
                decoded_line = ast.literal_eval(line)
                input_data = decoded_line['data']
                output_data = decoded_line['contents']
                # The order in which the input is given is the same order as the output data (ASSUMPTION FROM DATA COLLECTED, to make code more efficient)
                count = 0
                for key,value in input_data.iteritems():
                    items = output_data[0].keys()[0] if hasattr(output_data[0], 'keys') else output_data
                    output = output_data[count] if len(output_data)-1 > count else output_data
                    o.write(key+"\t"+repr(value)+"\t"+repr(items)+"\t"+str(output)+'\n')
                    count += 1
            except SyntaxError:
                ur_pattern = re.compile(r'((UNEXPECTED RESPONSE).*|(CONNECTION ERROR)).*')
                data_pattern = re.compile(r'\'data\':(.*),')
                ur_matched = ur_pattern.findall(line)
                data_matched = data_pattern.findall(line)
                o.write("Failed Packet \t Failed\t "+str(ur_matched)+"\t"+repr(str(data_matched))+"\n")
            o.flush()

    except IOError as inst:
            print(inst)
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
            # threadlock = threading.Lock()
            # threadlock.acquire()
            generate_excel_format(timestart)
            for fuzzThread in fuzz_threads:
                fuzzThread.stop()
            # threadlock.release()
            pass

# hue = random.randint(0, 65535)
# sat = random.randint(0, 255)
# bri = random.randint(0, 255)
# on = bool(random.getrandbits(1))
# inputs_list = {"bri": bri, "on": on, "hue": hue, "sat": sat}

# print generate_hue_inputs(inputs_list)
