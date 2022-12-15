import json
from itertools import groupby

class Graph:

    def __init__(self, G = None): #run evrey time class is called to create dictionarie

        self._valuelist = {}
        self._adjlist = {}

        if G != None: #run only if edges are given
            for edge in G: #make adjacency list from edges
                if edge[0] in self._adjlist:
                    self._adjlist[edge[0]].append(edge[1])
                else:
                    self._adjlist[edge[0]] = [edge[1]]
                if edge[1] in self._adjlist:
                    self._adjlist[edge[1]].append(edge[0])
                else:
                    self._adjlist[edge[1]] = [edge[0]]
            
            for key in self._adjlist:
                self._valuelist[key] = []


    def neighbours(self, vertex): #find neighbours
        return self._adjlist[vertex]

    def edges(self): #gives edges
        edges = []
        for key in self._adjlist:
            for key2 in self._adjlist[key]:
                if (key2, key) not in edges and (key, key2) not in edges:
                    edges.append((key, key2))
        return edges

    def vertices(self): #gives all nodes aka stops
        vertices = []
        for key in self._adjlist:
            vertices.append(key)
        return vertices

    def __len__(self): #amount of stops
        count = len(self._adjlist)
        return count

    def add_vertex(self, vertex): #adds vertex without neighbours
        if vertex not in self._adjlist:
            self._adjlist[vertex] = []
        return self._adjlist

    def add_edge(self, vertex1, vertex2): #adds edge between two stops
        if vertex1 in self._adjlist:
            self._adjlist[vertex1].append(vertex2)
        else:
            self._adjlist[vertex1] = [vertex2]
        if vertex2 in self._adjlist:
            self._adjlist[vertex2].append(vertex1)
        else:
            self._adjlist[vertex2] = [vertex1]
        return self._adjlist
    
    def remove_vertex(self, vertex): #removes stop from dictionary
        self._adjlist.pop(vertex)
        for key in self._adjlist:
            for i in range(len(self._adjlist[key])-1):
                if self._adjlist[key][i]==vertex:
                    self._adjlist[key].remove(vertex)
        return self._adjlist

    def remove_edge(self, vertex1, vertex2): #removes edge in dictionary
        self._adjlist[vertex1].remove(vertex2)
        self._adjlist[vertex2].remove(vertex1)
        return self._adjlist

    def get_vertex_value(self, vertex): #gets value
        return self._valuelist[vertex]

    def set_vertex_value(self, vertex, value): #sets value
        self._valuelist[vertex] = value
        return self._valuelist



class WeightedGraph(Graph):

    def __init__(self, G = None): #runs every time class called
        super(WeightedGraph, self).__init__(G)
        self._weightlist = {}
        edges = self.edges()
        for i in range(len(edges)):
            self._weightlist[edges[i]] = []


    def get_weight(self, vertex1, vertex2): #gets weigth between two vertices

        if (vertex1, vertex2) in self._weightlist:
            return self._weightlist[(vertex1, vertex2)]

        elif (vertex2, vertex1) in self._weightlist:
            return self._weightlist[(vertex2, vertex1)]


    def set_weight(self, vertex1, vertex2, weight): #sets weight
        self._weightlist[(vertex1, vertex2)] = weight
        return self._weightlist



def dijkstra(graph, source, cost=lambda u,v: 1): #shortest path finding algorithm
    
    g = graph
    dist = {} #dictionary of distance between stops
    prev = {} #previous stops, path
    unvisited = [] #list of unvisted stops

    for v in g.vertices():
        dist[v] = float('inf') #sets initial distance to inf for all stops

    unvisited = g.vertices() #all stops unvisited

    dist[source] = 0 #distance to source 0

    while unvisited != []: #runs while there are unvisted stops

        temp_dist = {}
        for stop in unvisited:
            temp_dist[stop] = dist[stop] #distance for unvisted stops

        min_val = min(temp_dist.values()) #find minimum distance for all unvisited stops
        current = [key for key in temp_dist if temp_dist[key] == min_val] #get key for minimum distance
        current = current[0] #if multiple elements, choose first

        unvisited.remove(current) #current now visited
        neighbour = g.neighbours(current) #gets neighbours to current

        for stop in neighbour: #loops over all neighbours
            if stop in unvisited: #unvisted stops
                alt = dist[current] + cost(current, stop) #graphs_weight.get_weight, alternative dist, dist to get to current plus dist to nieghbour
                if alt < dist[stop]: #save shortest dist
                    dist[stop] = alt
                    prev[stop] = current #save path

    dij = {} #djikstra dictionary

    for target in g.vertices():
        S = [] #stop sequence
        u = target #start at target

        if u in prev or u == source: #runs algorithm if path exists       
            while u in prev:   
                S.append(u) #add u to sequence                
                u = prev[u] #go to stop before, algorithm runs backwards
            S.append(source) #add source to sequence 
        path = {'path': S}
        dij[target] = path                   

    return dij



import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'


def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot'):

    import graphviz as gr
    dot = gr.Graph(name = 'Graph') #create dot object
    g = graph

    for v in g.vertices():
        if str(v) in nodecolors: #if v should be colored
            dot.node(str(v), fillcolor=nodecolors[str(v)], style = 'filled') #add node with color
        else:
            dot.node(str(v)) #add node without color

    edges = g.edges() #all edges
    for e in range(len(edges)): 
        dot.edge(str(edges[e][0]), str(edges[e][1])) #add edges to dot 

    dot.render(format='png', view=True) #view


def view_shortest(G, source, target, cost=lambda u,v: 1):

        path = dijkstra(G, source, cost)[target]['path']
        print(path)
        colormap = {str(v): 'darkseagreen' for v in path}
        print(colormap)
        visualize(G, view='view', nodecolors=colormap)

def demo():
    G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo()

