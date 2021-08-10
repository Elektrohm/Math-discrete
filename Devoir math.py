##Devoir de math discrète
##Implémenter l'algorithme de Dijkstra pour le problème de Wikispeedia

from collections import defaultdict
from urllib.parse import unquote
import os


def convert_to_adj(file_path):
    dico = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if (line[0] == '#' or line == "\n"):
                continue
            page,hyperlien = [unquote(item)for item in line.split()]
            dico[page] += [hyperlien]
    return dico

def dijkstra_shortest_path(graph,start,destination):
    number_of_nodes = len(graph)                                   
    to_visit = [start]                                                
    visited = [""]*number_of_nodes                              
    visited[0] = start                
    prev = [None]*number_of_nodes                                   
    
    while len(to_visit) != 0:                                        
        node = to_visit.pop(0)
        neighbours = graph[node]
        
        for following in neighbours:
            if graph.get(following,0)!=0:
                if following not in visited:
                    to_visit.append(following)
                    visited.append(following)
                    prev[list(graph.keys()).index(following)] = node
    
    path = []
    previous = destination
    while previous != None:
        path.append(previous)
        previous = prev[list(graph.keys()).index(previous)]
    path.reverse()
    if path[0]==start:
        return path
    return []

print(dijkstra_shortest_path(convert_to_adj("links.tsv"),"The_Simpsons","AK-47"))