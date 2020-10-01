import graph_tool.all as gt
import numpy as np
import time
import sys
from cp import cp

def FEAS(g, c, display=True): #Input: Graph g, clock period 'c' from D(u,v); Output: Clock period and optimal retiming found.  
                #For visualization purposes, the majority of graph drawings, sorts and other data outputs no more important 
                #than the clock period and the retiming is omitted to show a clean answer.
                #The notebook: 'RetimingProject_10670388_FEAS' shows the solution with more steps. 
    retimings = []
    for i in range(g.num_vertices()):
        retimings.append(0)
    #print(retimings)

    for i in range(g.num_vertices()-1):
    
        #We proceed to calculate the new retiming weights.
        gFinal = gt.Graph(g)
        #print(gFinal)

        for edge in gFinal.edges():
            source = int(str(edge.source())) #Get source node from edge.
            target = int(str(edge.target())) #Get target node from edge.
            gFinal.ep.weight[edge] = gFinal.ep.weight[edge] + retimings[target] - retimings[source] 

        #Compute Clock Period Algorithm (Algorithm CP)
            
        solution = cp(gFinal)[0]
      
        for vertex in solution.vertices():
            if (solution.vp.delta[vertex]>c):
                retimings[int(vertex)] = retimings[int(vertex)] + 1 #Get new Retimings.

        #print(retimings)

    #Perform algorithm CP Again. 
    
    clockPeriod = cp(solution)[1]
    
    #print("FEAS Algorithm finished with c: "+str(c))
    #print("Clock Period of the graph is: " + str(clockPeriod))

    if (display):
        if (clockPeriod > c):
            print("No feasible retiming exists.")
        else:
            print("Retiming: %s is the desired retiming." % (retimings))
        
    return clockPeriod, retimings