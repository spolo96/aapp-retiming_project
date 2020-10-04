from RetimingProject_Main import *
from memory_profiler import memory_usage
from memory_profiler import profile

# TestProfiler (with Lists instead of NumpyArrays)
opt1x = []
opt1y = []
opt2x = []
opt2y = []


def memoryProfiler():
    for i in range(5):
        x = (i+1)*10
        g = graphCorrelator(x)

        # OPT1
        memUsage = memory_usage(OPT1(g,False), interval=.2, timeout=1)
        average = sum(memUsage) / len(memUsage)
        average = round(average, 2)

        opt1x.append(x)
        opt1y.append(average)

        # OPT2
        memUsage = memory_usage(OPT2(g, False), interval=.2, timeout=1)
        average = sum(memUsage) / len(memUsage)
        average = round(average, 2)

        opt2x.append(x)
        opt2y.append(average)


memoryProfiler()
showMemoryGraph(opt1x, opt1y, opt2x, opt2y)


#showMemoryGraph(opt1x, opt1y, opt2x, opt2y)
