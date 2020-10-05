from RetimingProject_Main import *
from memory_profiler import memory_usage
import sys

if(len(sys.argv)<=2):
    print("Error. You must specify the value to iterate. E.g: python3 profiler.py generator/correlator 10")
else:
    #TestProfiler (with Lists instead of NumpyArrays)
    opt1x = []
    opt1y = []
    opt1ymb = []
    opt2x = []

    opt2y = []
    opt2ymb = []

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
        memUsage = memory_usage(OPT1(g,False), interval=.2, timeout=1)
        average = sum(memUsage) / len(memUsage)
        average = round(average, 2)
        end = time.time()
        y = end-start

        opt1x.append(x)
        opt1y.append(y)
        opt1ymb.append(average)

        #OPT2
        start = time.time()
        memUsage = memory_usage(OPT2(g,False), interval=.2, timeout=1)
        average = sum(memUsage) / len(memUsage)
        average = round(average, 2)
        end = time.time()
        y = end-start

        opt2x.append(x)
        opt2y.append(y)
        opt2ymb.append(average)

    showTimeGraph(opt1x, opt1y, opt2x, opt2y)
    showMemoryGraph(opt1x,opt1ymb,opt2x,opt2ymb)