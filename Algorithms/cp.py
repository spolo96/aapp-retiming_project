import graph_tool.all as gt
import numpy as np
import time
import sys

def cp(graph, display=False):
    g0 = gt.Graph(graph)
    
    removedEdges = []

    for edge in g0.edges():
        if (g0.ep.weight[edge]!=0):
            removedEdges.append([edge.source(),edge.target()])

    delta = g0.new_vertex_property("int") #Property delta(node) in the reference paper.

    g0.vertex_properties["delta"] = delta
    
    delta = np.zeros(g0.num_vertices())

    for i in range(len(removedEdges)):
        g0.remove_edge(g0.edge(removedEdges[i][0], removedEdges[i][1]))

    if(display):
        gt.graph_draw(g0, vertex_text=g0.vp.cap, edge_text=g0.ep.weight)
        
    #Topological Sort
    tree = gt.min_spanning_tree(g0)
    g0.set_edge_filter(tree)
    sort = gt.topological_sort(g0)
    if (display):
        print(sort)
    
    #Calculate Clock Period of the Graph:
    for node in sort:

        if (g0.vertex(node).in_degree()==0): #If the node doesn't have incoming edges. 
             g0.vp.delta[node] = g0.vp.cap[node]
        else:
            maxDelta = 0
            for edge in g0.vertex(node).in_edges():
                if (g0.vp.delta[g0.vertex(edge.source())] > maxDelta):
                    maxDelta = g0.vp.delta[g0.vertex(edge.source())]

            g0.vp.delta[node] = g0.vp.cap[node] + maxDelta

    clockPeriod = 0
    for node in sort:
        if (g0.vp.delta[node] > clockPeriod): #Update clock period 
            clockPeriod = g0.vp.delta[node]

    if(display):
        print("Clock Period of the graph is: " + str(clockPeriod))
    
    return g0, clockPeriod