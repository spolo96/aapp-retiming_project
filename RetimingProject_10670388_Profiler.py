import graph_tool.all as gt
import numpy as np
import time

#Implemented Algorithms
def WD(graph): #Algorithm WD that computes both the W and the D matrix from a known graph. 
    W = np.zeros((graph.num_vertices(),graph.num_vertices())) #Initialize W Matrix
    D = np.zeros((graph.num_vertices(),graph.num_vertices())) #Initialize D Matrix
    #print(W)
    #print(D)

    g2 = gt.Graph(graph) #Copy the graph to perform other operations.

    ordered_pair = g2.new_edge_property("vector<int>")
    g2.edge_properties["weight_pair"] = ordered_pair

    for edge in graph.edges():
        g2.ep.weight_pair[edge] = [graph.ep.weight[edge], graph.vp.cap[edge.source()]*(-1)]
    
    for i in range(graph.num_vertices()):
        for j in range(graph.num_vertices()):
            if (i!=j): #Exclude the same node path calculation.
                #Calculate the total weight of the path we just got.
                path = gt.shortest_path(g2, i, j)
                weightSum = [0,0] #Ordered pair weightSum [x,y] that will be: [w(e), -d(u)]
                for item in path[1]:
                    #print(item)
                    weightSum = [weightSum[0] + g2.ep.weight_pair[item][0], weightSum[1] + g2.ep.weight_pair[item][1]]

                #print(weightSum)
                #Coge weightSum y haz las respectivas operaciones con (x,y); W(u,v) y D(u,v)              

                W[i][j] = weightSum[0] #W(u,v) = x 
                #print(W[i][j])

                D[i][j] = g2.vp.cap[j] - weightSum[1] #D(u,v) = d(v) -y
                #print(D[i][j])
            else:
                D[i][j] = graph.vp.cap[graph.vertex(i)]


    print("W Matrix: ")
    print(W)
    print("D Matrix: ")
    print(D)
    return [W,D]

def OPT1(g):
    tupleWD = WD(g) #Perform W and D matrix computation for the algorithm
    W = tupleWD[0]
    D = tupleWD[1]
    copyD = np.copy(D) #This is the array we will sort. 
    copyD = np.unique(copyD)
    #r(u) - r(v) <= w(e)
    optimalRetiming = []
    
    minimumClockPeriod = 999
    for i in range(len(copyD)):     #Gets calculated with sorted D(u,v)

        c = copyD[i]
        
        print("Test with C: "+str(c))
        
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
                        if(not( (D[node1][node2] - g5.vp.cap[node1] > c) or (D[node1][node2] - g5.vp.cap[node2] > c))):
                            e = g5.add_edge(node1,node2)
                            g5.ep.weight[e] = W[node1][node2] - 1

        #(Inequalities)
        minPathSums = [] #Initialize the array of Minimum Path Sums
        minPath = []

        for i in range(nodesSize):
            minPathSums.append(999)

        isPossible = True #Flag in order to know if there is not any violation in the constraints. 
        for i in range(nodesSize):
            if (isPossible):
                try:
                    path = gt.shortest_path(g5, nodesSize, i, weights=g5.ep.weight, negative_weights=True) 
                    #print(path)
                    pathSum = 0 

                    for item in path[1]:        
                        pathSum = pathSum + g5.ep.weight[item] 

                    if (pathSum < minPathSums[i]):
                            minPathSums[i] = pathSum
                            minPath = path
                            
                    print("Variable: %s , value: %s " % (i,minPathSums[i]))
                    #print("Minimum path:")
                    #print(minPath)
                except ValueError: 
                    isPossible = False
                    print("Negative Loops Found. Skipping Solution...")

        if (isPossible):
            #Now that we found a solution to the Linear Inequalities, we proceed to calculate the new retiming weights.

            for i in range(len(minPathSums)):
                print(minPathSums[i])
                        
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
                print("Edge: %s with new value: %s" % (edge, gFinal.ep.weight[edge]))

            #New Graph Gr
            print("New Graph Gr: ")
            gt.graph_draw(gFinal, vertex_text=gFinal.vertex_index, edge_text=gFinal.ep.weight)
            
            g0 = gt.Graph(gFinal)

            removedEdges = []

            for edge in g0.edges():
                if (g0.ep.weight[edge]!=0):
                    removedEdges.append([edge.source(), edge.target()])

            #print(removedEdges)
            #print(len(removedEdges))

            delta = g0.new_vertex_property("int") #Property delta(node) in the reference paper.

            for i in range(len(list(g0.vertices()))):
                delta[i] = 0

            g0.vertex_properties["delta"] = delta

            #print(removedEdges[0][0])
            #print(removedEdges[0][1])

            for i in range(len(removedEdges)):
                g0.remove_edge(g0.edge(removedEdges[i][0], removedEdges[i][1]))
            
            print("Graph G0 taken from Gr: ")
            gt.graph_draw(g0, vertex_text=g0.vp.cap)

            #Topological Sort
            sortedGraph = gt.Graph(g0)
            tree = gt.min_spanning_tree(g0)
            g0.set_edge_filter(tree)
            sort = gt.topological_sort(g0)
            #print(sort)

            for node in sort:

                if (g0.vertex(node).in_degree()==0): #If the node doesn't have incoming edges. 
                    g0.vp.delta[node] = g0.vp.cap[node]
                else:
                    maxDelta = 0
                    for edge in g0.vertex(node).in_edges():
                        if (g0.vp.delta[g0.vertex(edge.source())] > maxDelta):
                            maxDelta = g0.vp.delta[g0.vertex(edge.source())]

                    g0.vp.delta[node] = g0.vp.cap[node] + maxDelta

            #print(g0.vp.delta[node])

            clockPeriod = 0
            for node in sort:
                if (g0.vp.delta[node] > clockPeriod): #Update clock period 
                    clockPeriod = g0.vp.delta[node]

            print("Clock Period of the graph is: %s with value of c as: %s" % (clockPeriod, c))
            if (clockPeriod < minimumClockPeriod):
                minimumClockPeriod = clockPeriod
                clockPeriodFound = c
                optimalRetiming = minPathSums

    print("Minimum Clock Period is: %s with c: %s" % (minimumClockPeriod, clockPeriodFound))
    return optimalRetiming

#Examples:
#Example taken from: https://people.eecs.berkeley.edu/~keutzer/classes/244fa2005/lectures/8-2-retiming-ucb.pdf and 
#SummerSessionProjectAA.pptx
g = gt.Graph()

edge_weight = g.new_edge_property("double")
g.edge_properties["weight"] = edge_weight
edge_str_weight = g.new_edge_property("string")

vlist = g.add_vertex(4) #Creation of vertices

edges = [[0,1],[1,2],[1,3],[2,3],[3,0]] #array of Edges 

nodeCapacity = [0,3,3,7] #Aka "d(node_i)" #Array d(v) in the paper (Propagation delay)

cap = g.new_vertex_property("int")

weights = [2,0,0,0,0] #array of weights "w" (Register count) 

for i in range(len(list(vlist))):
    cap[i] = nodeCapacity[i]

g.vertex_properties["cap"] = cap    #Array d(v) in the paper (Propagation delay)

for i in range(len(edges)):
    e = g.add_edge(edges[i][0], edges[i][1])
    g.ep.weight[e] = weights[i]
    edge_str_weight[e] = str(weights[i])
    
print(g)
gt.graph_draw(g, vertex_text=g.vp.cap, edge_text=edge_str_weight)

for v in g.vertices():
    print("Vertex %s with capacity: %s" % (v, g.vp.cap[v]))
    
print(g.list_properties())

print("OPT1: ")
print(OPT1(g))


