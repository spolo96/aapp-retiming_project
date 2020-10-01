import graph_tool.all as gt
import numpy as np
import time
import sys
from wd import WD
from feas import FEAS

def OPT2(graph): #Algorithm OPT2 from the Reference paper. Complexity of the algorithm in O(|V| |E| lg |V|) time.
    tupleWD = WD(graph) #Perform W and D matrix computation for the algorithm
    W = tupleWD[0]
    D = tupleWD[1]
    copyD = np.copy(D) #This is the array we will sort. 
    copyD = np.unique(copyD)
    minimumClockPeriod = sys.maxsize
    optimalRetiming = []
    for i in range(len(copyD)): 

        c = copyD[i]
        #print("Test with C: "+str(c))
        
        solution = FEAS(graph,c) #Execute FEAS Algorithm that will give us a tuple = [clock_period, retimings]
        
        clockPeriod = solution[0]
        retimings = solution[1]
       
        #print("Clock Period of the graph (OPT2) is: %s" % (clockPeriod))
        
        #if (clockPeriod > c):
         #   print("No feasible retiming exists.")
        #else:
         #   if(clockPeriod < minimumClockPeriod):
          #      minimumClockPeriod = clockPeriod
           #     optimalRetiming = retimings
            #    print("Retiming: %s is the desired retiming." % (retimings))
            #else:
             #   print("It doesn't improve the retiming.")
                
        if (clockPeriod <= c):
            if(clockPeriod < minimumClockPeriod):
                minimumClockPeriod = clockPeriod
                optimalRetiming = retimings
                #print("Retiming: %s is the desired retiming." % (retimings))
            #else:
                #print("It doesn't improve the retiming.")

    print("Minimum Achievable Clock Period is: %s with retiming: %s" % (minimumClockPeriod, optimalRetiming))
    return minimumClockPeriod, optimalRetiming