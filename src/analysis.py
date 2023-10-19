import json
import matplotlib.pyplot as plt
import networkx as nx
from scipy import *


filename = 'results.json'
with open(filename, 'r') as f:
    experiments = json.load(f)


minPathSizes = []

foundMap = {
    'found': 0,
    'notFound': 0
}

bestInSteps = {
    'bfs': [],
    'aStar': [],
    'equal': 0
}

def graphAnalysis(graph):
    G = nx.Graph()

    for key in graph.keys():
        for neighbor in graph[key].neighbors:
            G.add_edge(key, neighbor)

    # plt.plot(degree_sequence, "b-", marker="o")
    # plt.title("Degree Rank Plot")
    # plt.ylabel("Degree")
    # plt.xlabel("Rank")
    # plt.savefig('../figures/graph_degree_rank.png', dpi=300, bbox_inches='tight')

    centrality = nx.degree_centrality(G)
    firstNCentrality = list(centrality.items())[:2000]
    actorsName = []
    actorsCentrality = []
    for key in firstNCentrality:
        actorsName.append(graph[key[0]].name)
        actorsCentrality.append(key[1])
    plt.bar(actorsName, actorsCentrality)
    plt.title('Actors Centrality')
    plt.xlabel('Actor')
    plt.ylabel('Centrality')
    plt.savefig('../figures/actors_centrality.png', dpi=300, bbox_inches='tight')
    
    
def experimentAnalysis():

    for src in experiments:
        if src['bfs']['cost'] != -1:
            foundMap['found'] += 1
            if src['bfs']['steps'] < src['a_star']['steps']:
                bestInSteps['bfs'].append(src['a_star']['steps'] - src['bfs']['steps'])
            elif src['a_star']['steps'] < src['bfs']['steps']:
                bestInSteps['aStar'].append(src['bfs']['steps'] - src['a_star']['steps'])
            else:
                bestInSteps['equal'] += 1
        else:
            foundMap['notFound'] += 1


    plt.bar(bestInSteps.keys(), [len(x) if type(x) == list else x for x in bestInSteps.values()])
    plt.title('BFS x AStar - Path found with least iteractions')
    plt.xlabel('Algorithm')
    plt.ylabel('Actors (source -> target)')
    plt.savefig('../figures/path_found_least_iteractions.png', dpi=300, bbox_inches='tight')

    plt.bar(foundMap.keys(), foundMap.values())
    plt.title('BFS x AStar - Path was found')
    plt.xlabel('Path found')
    plt.ylabel('Actors (source -> target)')
    plt.savefig('../figures/path_found.png', dpi=300, bbox_inches='tight')