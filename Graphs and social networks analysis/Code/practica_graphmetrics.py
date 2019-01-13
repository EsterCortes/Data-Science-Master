
# PAULA CARBALLO PÉREZ Y ESTER CORTÉS GARCÍA
import community
import networkx as nx
from networkx.readwrite import json_graph
import json
import matplotlib.pyplot as plt
import operator

with open("graph.json","r") as f:
    # Carga el grafo
    json_data = json.load(f)
    g = json_graph.node_link_graph(json_data,directed=False)
    # Métricas generales
    i = 1
    for comp in nx.connected_component_subgraphs(g):
        print('Comp ', i, ': ') #En nuestro caso sólo hay una componente conexa
        i += 1
        print('\tSize:', len(comp.nodes()))
        if len(comp.nodes()) > 1:
            #degreeCent = nx.degree_centrality(comp)
            closeness = nx.closeness_centrality(comp)
            betweenness = nx.betweenness_centrality(comp)
            pagerank = nx.pagerank(comp)
            #print('\tDegree:', degreeCent)
            #print('\tMAX DEG: ', max(degreeCent.items(), key=operator.itemgetter(1)))
            print('\tCloseness:', closeness)
            print('\tMAX CLOSENESS: ', max(closeness.items(), key=operator.itemgetter(1)))
            print('\tBetweenness:', betweenness)
            print('\tMAX BETWEENNESS: ', max(betweenness.items(), key=operator.itemgetter(1)))
            print('\tPageRank:', pagerank)
            print('\tMAX PAGERANK: ', max(pagerank.items(), key=operator.itemgetter(1)))

    # Comunidades
    partition = community.best_partition(g)
    print(partition)
    '''for elem in partition:
        print(elem + ":" + str(partition[elem]))'''
    # Dibujo
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(g)
    count = 0.
    for com in set(partition.values()):
        count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                  if partition[nodes] == com]
    nx.draw_networkx_nodes(g, pos, list_nodes, node_size=20,
                           node_color=str(count / size))

    nx.draw_networkx_edges(g, pos, alpha=0.5)
    plt.show()
