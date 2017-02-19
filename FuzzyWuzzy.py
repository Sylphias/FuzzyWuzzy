import sys,getopt, radamsa, LogToExcel
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
        # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
            # process arguments
    for arg in args:
        runFuzzer(sys.argv[0],opts)
        # process(arg)  # process() is defined elsewhere

    if __name__ == "__main__":
        main()


def runFuzzer(fuzzer, *args):
    # args[0] - for options
    # args[1] - payload file that contains json/inputs that are to be mutated in a dictionary
    if fuzzer == "radamsa":
        radamsa(args[0], args[1])
    elif fuzzer == "parse":
        LogToExcel.generate_excel_format_hue(args[1])



if __name__ == "__main__": main()
