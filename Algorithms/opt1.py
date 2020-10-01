import graph_tool.all as gt
import numpy as np
import time
import sys
from wd import WD
from cp import cp

def OPT1(g):
    tupleWD = WD(g) #Perform W and D matrix computation for the algorithm #Step 1 from OPT1.
    W = tupleWD[0]
    D = tupleWD[1]
    copyD = np.copy(D) #This is the array we will sort. 
    copyD = np.unique(copyD) #Step 2 from OPT1.
    #r(u) - r(v) <= w(e)
    optimalRetiming = []
    
    minimumClockPeriod = sys.maxsize
    for i in range(len(copyD)):     #Gets calculated with sorted D(u,v)

        c = copyD[i]
        
        g5 = gt.Graph(g) #Create a copy of the graph in order to perform other operations. 

        nodesSize = g5.num_vertices() #Get the number of the nodes.

        g5.add_vertex() #Add new artificial node to perform the shortest-path. 

        for i in range(nodesSize):
            e = g5.add_edge(nodesSize, i) #We add the nodesSize number-index as the new node for the Bellman Ford algorithm.
            g5.ep.weight[e] = 0

        for edge in g5.edges(): #Visualization purposes. #Theorem 7.1 in the Reference Paper.
            if (edge.source()!=nodesSize and edge.target()!=nodesSize):

                #print("r(u): %s, r(v): %s with edge: %s" % (edge.source(), edge.target(), edge_weight[edge]))

                source = int(str(edge.source()))
                target = int(str(edge.target()))

        for node1 in range(g5.num_vertices()): #Theorem 7.2 in the Reference Paper.
            for node2 in range(g5.num_vertices()):

                if (node1!=node2 and node1!= nodesSize and node2!= nodesSize):
                    if (D[node1][node2] > c):
                            e = g5.add_edge(node1,node2)
                            g5.ep.weight[e] = W[node1][node2] - 1
        
        edgeRemoval = []
        for edge in g5.edges():
            node1 = int(str(edge.source()))
            node2 = int(str(edge.target()))
            if (node1!=node2 and node1!= nodesSize and node2!= nodesSize):
                if( ( (D[node1][node2] - g5.vp.cap[node1]) > c) or ( (D[node1][node2] - g5.vp.cap[node2]) > c) ):
                                edgeRemoval.append(edge)
                    
        #DELETION OF EDGES
        for i in range(len(edgeRemoval)):
            g5.remove_edge(edgeRemoval[i])
        
        #(Inequalities)
        minPathSums = [] 
        minPath = []
        
        #gt.graph_draw(g5, vertex_text=g5.vertex_index, edge_text=g5.ep.weight)
        
        for i in range(nodesSize): #Initialize the array of Minimum Path Sums
            minPathSums.append(sys.maxsize)

        isPossible = True #Flag in order to know if there is not any violation in the constraints. 
        for i in range(nodesSize):
            isPossible = True
            if (isPossible):
                try:
                    path = gt.shortest_path(g5, nodesSize, i, weights=g5.ep.weight, negative_weights=True) 
                    
                    pathSum = 0 

                    for item in path[1]:        
                        pathSum = pathSum + g5.ep.weight[item] 

                    if (pathSum < minPathSums[i]):
                            minPathSums[i] = pathSum
                            minPath = path
                            
                except ValueError: 
                    isPossible = False
                    #print("Negative Loops Found. Skipping Solution...")

        if (isPossible):
            #Now that we found a solution to the Linear Inequalities, we proceed to calculate the new retiming weights.

            #for i in range(len(minPathSums)):
                #print(minPathSums[i])
                        
            gFinal = gt.Graph(g)
                #print(gFinal)

            for edge in gFinal.edges():
                source = int(str(edge.source()))
                target = int(str(edge.target()))
                gFinal.ep.weight[edge] = gFinal.ep.weight[edge] - minPathSums[target] + minPathSums[source] 
                #The reason the subtraction is swapped here is because the edges for the Bellman-Ford algorithm 
                #were created in the inverse order for simplification purposes.
                #By replacing the target and the source operation, we get the original operation with values that satisfy
                #the Theorem 7. 
                #print("Edge: %s with new value: %s" % (edge, gFinal.ep.weight[edge]))

            #New Graph Gr
            #print("New Graph Gr: ")
            #gt.graph_draw(gFinal, vertex_text=gFinal.vertex_index, edge_text=gFinal.ep.weight)
            
            clockPeriod = cp(gFinal)[1]
            #print("clockPeriod: %s" % (clockPeriod))

            #print("Clock Period of the graph is: %s with value of c as: %s" % (clockPeriod, c)) #ERASED PROFILING
            if (clockPeriod < minimumClockPeriod):
                minimumClockPeriod = clockPeriod
                clockPeriodFound = c
                optimalRetiming = minPathSums

    print("Minimum Clock Period is: %s" % (minimumClockPeriod))
    print("Retiming: %s" % (optimalRetiming))
    return optimalRetiming