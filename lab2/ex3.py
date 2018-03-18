'''Come prima cosa determinate dei valori di n, p e m tali che la procedura ER e la procedura UPA generino un grafo
con lo stesso numero di nodi ed un numero di archi simile a quello della rete reale.

Quindi, per ognuno dei tre grafi (rete reale, ER, UPA), simulate un attacco che disabiliti i nodi
della rete uno alla volta seguendo un ordine casuale, fino alla disattivazione di tutti i nodi del grafo,
e calcolate la resilienza del grafo dopo ogni rimozione di un nodo.

Dopo aver calcolato la resilienza dei tre grafi, mostrate il risultato in un grafico con scala
lineare (non log/log) che combini le tre curve ottenute. Usate un grafico a punti oppure a linea
per ognuna delle curve.
L'asse orizzontale del grafico deve corrispondere al numero di nodi disattivati dall'attacco (che variano da 0 a n),
mentre l'asse verticale alla dimensione della componente connessa piu grande rimasta dopo aver rimosso un certo numero di nodi.
Aggiungete una legenda al grafico che permetta di distinguere le tre curve e che specifici i valori di p e m utilizzati.
Allegate il file con la figura nell'apposito spazio.'''

from utils.graphGenerator import graphGenerator
from utils.resilienceCount import maxCC, DFSVisited
import random
import matplotlib.pyplot as plp
from sys import setrecursionlimit

n = 1476
p = 0.003 #(n archi*100/n^2)
m = 3
path = "as19991212.txt"
setrecursionlimit(10000)

def mostImportantNodeAttack(graph,size_max):
    # print("Graph to attack: ",graph.adj_list)
    # most important node
    m_i_node = -1
    # adj_list del most_important node
    m_i_adj_list = set()
    # size della adj_list del most important node
    m_i_node_size_adj_list = -1
    # True sse abbiamo trovato una adj_list della massima dimensione possibile, ovvero |V| - 1
    find = False

    # cerca il nodo con la adj_list maggiore, ovvero il nodo piu importante
    if graph and graph.adj_list:
        for nodes in graph.adj_list:
            if find == False: # purtroppo python non supporta i foreach-loop con piu di una condizione ...
                current_node_size_adj_list = len(graph.adj_list[nodes])
                if current_node_size_adj_list > m_i_node_size_adj_list:
                    m_i_node = nodes
                    m_i_node_size_adj_list = current_node_size_adj_list
                    m_i_adj_list = graph.adj_list[nodes]
                # se abbiamo trovato una adj_list di grandezza size_max, allora non serve piu iterare: non possono esistere adj_list maggiori
                if m_i_node_size_adj_list == size_max:
                    find = True

    # rimuovo il nodo piu importante da tutte le liste delle adj nel quale compare
    for nodes in m_i_adj_list:
        if m_i_node in graph.adj_list[nodes]: # TODO: ma questo controllo serve??
            graph.adj_list[nodes].remove(m_i_node)

    # infine rimuovo la chiave corrispondente al nodo piu importante
    graph.adj_list.pop(m_i_node, None)
    # print("final graph: ",graph.adj_list)
    resilience = maxCC(graph)
    return resilience

# invoca mostImportantNodeAttack fino alla disabilitazione totale dei nodi
def killTheNetwork(graph):
    resilience = [maxCC(graph)]
    while graph and graph.adj_list:
        resilience.append(mostImportantNodeAttack(graph,n-1))
    return resilience

all_graphs = graphGenerator(path,n,p,m)
ERgraph = all_graphs.ER_graph
generalGraph = all_graphs.graph_from_file
UPAgraph = all_graphs.UPA_graph

resilience_general = killTheNetwork(generalGraph)
resilience_ER = killTheNetwork(ERgraph)
resilience_UPA = killTheNetwork(UPAgraph)

plp.grid()
plp.plot(resilience_general, label = "General Graph")
plp.plot(resilience_ER, label = "ER Graph p = " + str(p))
plp.plot(resilience_UPA, label = "UPA Graph m = " + str(m))
plp.xlabel('The number of nodes removed')
plp.ylabel('Size of largest connected component after node removal')
plp.title('The resilience of General, ER and UPA Graphs')
plp.legend()
plp.show()
