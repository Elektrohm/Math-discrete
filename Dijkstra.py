from collections import defaultdict
from urllib.parse import unquote
"""# Convertir un string
new_utf8_string = unquote(old_url_string)
# Convertir une liste de strings
new_utf8_list = [unquote(item) for item in old_url_list]"""

def convert_to_adj(file_path):
    dico = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if (line[0] == '#' or line == "\n"):
                continue
            page,hyperlien = [unquote(item)for item in line.split()]
            dico[page] += [hyperlien]
    return dico

"""Liste vide s'il n'y a pas de chemin entre start et destination OU
Liste de strings avec hyperliens formant le plus court chemin si un chemin existe (ex: ["The_Simpsons", "Alcohol", "Metal", "Corrosion"])"""

def dijkstra_shortest_path(graph, start, destination):
    if start == destination :
        return [start]
    elif start not in graph or destination not in graph :
        return []
    else :
        ways = []
        for word in graph[start] :
            ways.append([start, word]) 
        while True :
            for way in ways :
                if destination in way :
                    return way
                else :
                    for elem in graph[way[-1]] :
                        if elem not in way :
                            i = way.copy() + [elem]
                            ways.append(i)
                    ways.remove(way)
        

print("test launched")
print(dijkstra_shortest_path(convert_to_adj('links.tsv'), "Saint_Helena", "Ceasar_cipher"))

"""
from collections import defaultdict
from urllib.parse import unquote
import os


def convert_to_adj(file_path):
    d = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line[0] == '#' or line == "\n":
                continue
            else:
                u,v = line.split()
                u = unquote(u)
                v = unquote(v)
                d[u].append(v)

    return d


def dijkstra_shortest_path(graph, start, destination):
    index = 0
    dic = {}
    for str in graph:
        if str not in dic:
            dic[str] = index
            index += 1
        for foo in graph[str]:
            if foo not in dic:
                dic[foo] = index
                index += 1

    size = index
    dist = [0] * size
    parent = [""] * size

    queue = []
    queue.append(start)
    dist[dic[start]] = 1

    while len(queue) > 0:
        s = queue.pop(0)
        for i in graph[s]:
            if dist[dic[i]] == 0:
                dist[dic[i]] = dist[dic[s]] + 1
                if (i in graph):
                    queue.append(i)
                parent[dic[i]] = s


    if dist[dic[destination]] == 0:
        return []
    else:
        rep = []
        rep.append(destination)
        while rep[-1] != start:
            rep.append(parent[dic[rep[-1]]])
        rep.reverse()
        return rep


# print([""])
print(convert_to_adj("links.tsv"))
#print(dijkstra_shortest_path(convert_to_adj("links.tsv"), "The_Simpsons", "Corrosion"))
"""
