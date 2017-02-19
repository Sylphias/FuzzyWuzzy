import re, ast
def generate_excel_format_hue(timestamp):
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


if __name__ == "__main__":
    generate_excel_format_hue("2017-029194510")