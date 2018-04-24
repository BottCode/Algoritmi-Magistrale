from utils.graphFromFile import graphFromFile
import os
from math import inf
import time as T
import sys #libreria per interrompere l'esecuzione

def HKTSP(graph):

    V = frozenset([x for x in range(1,graph.Dimension + 1)])
    t0 = T.time()
    return HKVisit(1,V,graph,t0,V)

def HKVisit(v,S,graph,t0,V):



            #
    if S == {v}:
        return graph.adj_list[v-1][0] #graph.CalcDistance(v,1,graph.getWeightType())
    elif (v,S) in graph.d and graph.d[(v,S)] != None:
        return graph.d[(v,S)]
    else:
        min_dist = inf
        min_prec = None
        for u in (S - {v}):
            dist = HKVisit(u,S - {v},graph,t0,V)
            relax_val = dist + graph.adj_list[u-1][v-1]#graph.CalcDistance(u,v, graph.getWeightType())
            if relax_val < min_dist:
                min_dist = relax_val
                min_prec = u
                graph.d[(v,S)] = min_dist
                graph.pi[(v,S)] = min_prec
                if (S == V - {1}):
                    print(graph.d[(1,V - {1})])



        #if T.time() - t0 > 120: #dopo x secondi
        #    print(graph.d[(1,V)])
        #    sys.exit("Esecuzione terminata")

        return min_dist

graph = graphFromFile("graphs/berlin52.tsp")

res = HKTSP(graph)
#V = frozenset([x for x in range(1,graph.Dimension + 1)])
#print(graph.d[(1,V)])
print("RESULT",res)

'''# itero su tutti i file in graphs che terminano con .tsp
for filename in os.listdir("graphs/"):
    if filename.endswith(".tsp"):
        graph = graphFromFile("graphs/"+filename)
        res = HKTSP(graph)'''
