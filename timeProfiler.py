from RetimingProject_Main import *
from memory_profiler import memory_usage

import sys

if(len(sys.argv)<=2):
    print("Error. You must specify the value to iterate. E.g: python3 timeProfiler.py correlator/generator 10")
else:
    opt1x = []
    opt1y = []
    opt2x = []
    opt2y = []

    for i in range(int(sys.argv[2])):
        x = (i+1)*10

        if (sys.argv[1] == "generator"):
            g = graphGenerator(x)
        elif (sys.argv[1] == "correlator") :
            g = graphCorrelator(x)

        else:
            print("Error. You should test the profiler with either graph generator or correlator.")
            print("Example: python3 profiler.py generator/correlator 10")
            break

        #OPT1
        start = time.time()
        OPT1(g)
        end = time.time()
        y = end-start

        opt1x.append(x)
        opt1y.append(y)

        #OPT2
        start = time.time()
        OPT2(g)
        end = time.time()
        y = end-start

        opt2x.append(x)
        opt2y.append(y)
        showTimeGraph(opt1x, opt1y, opt2x, opt2y)

