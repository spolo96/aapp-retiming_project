from RetimingProject_Main import *
from memory_profiler import memory_usage

#TestProfiler (with Lists instead of NumpyArrays)
opt1x = []
opt1y = []
opt2x = []
opt2y = []

for i in range(5):
    x = (i+1)*10
    g = graphCorrelator(x)

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