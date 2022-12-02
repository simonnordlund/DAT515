import json
from itertools import groupby

class Graph():

    def __init__(self, G): #run evrey time class is called to create dictionarie
        self._valuelist = {}
        self._adjlist = {}

        self.temp = {k: [v[1] for v in g] for k, g in groupby(sorted(G), lambda e: e[0])}
        self._adjlist = {k: [v[1] for v in g] for k, g in groupby(sorted(G), lambda e: e[0])}

        for key in self.temp:
            for item in self.temp[key]:
                print(self._adjlist)
                print(item)
                if item in self._adjlist:
                    self._adjlist[item].append(key)
                else:
                    self._adjlist[item] = [key]
        
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
        if isinstance(vertex, list):
            for i in range(len(vertex)):
                self._valuelist[vertex[i]] = value
        else:
            self._adjlist[vertex] = value
        return self._valuelist


    class WeightedGraph():

        def __init__(self): #runs every time class called
            self._weightlist = {}
            edges = self.edges()
            for i in range(len(edges)):
                self._weightlist[edges[i]] = []

        def get_weight(self, vertex1, vertex2): #gets weigth between two vertices 
            return self._weightlist[(vertex1, vertex2)]

        def set_weight(self, vertex1, vertex2, weight): #sets weight
            self._weightlist[vertex1, vertex2] = weight
            return self._weightlist



    def dijkstra(self, graph, source, cost=lambda u,v: 1): #shortest path finding algorithm
        
        dist = {} #dictionary of distance between stops
        prev = {} #previous stops, path
        unvisited = [] #list of unvisted stops

        for v in self.vertices():
            dist[v] = float('inf') #sets initial distance to inf for all stops

        unvisited = self.vertices() #all stops unvisited

        dist[source] = 0 #distance to source 0

        while unvisited != []: #runs while there are unvisted stops

            temp_dist = {}
            for stop in unvisited:
                temp_dist[stop] = dist[stop] #distance for unvisted stops

            min_val = min(temp_dist.values()) #find minimum distance for all unvisited stops
            current = [key for key in temp_dist if temp_dist[key] == min_val] #get key for minimum distance
            current = current[0] #if multiple elements, choose first

            unvisited.remove(current) #current now visited
            neighbour = self.neighbours(current) #gets neighbours to current

            for stop in neighbour: #loops over all neighbours
                if stop in unvisited: #unvisted stops
                    alt = dist[current] + cost[current][stop] #graphs_weight.get_weight, alternative dist, dist to get to current plus dist to nieghbour
                    if alt < dist[stop]: #save shortest dist
                        dist[stop] = alt
                        prev[stop] = current #save path

        dji = {} #djikstra dictionary

        for target in self.vertices():
            S = [] #stop sequence
            u = target #start at target

            if u in prev or u == source: #runs algorithm if path exists       
                while u in prev:   
                    S.append(u) #add u to sequence                
                    u = prev[u] #go to stop before, algorithm runs backwards
                S.append(source) #add source to sequence 
            path = {'path': S}
            dji[target] = path                   

        return dji





with open('tramnetwork.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)
    weight = data['times']

#print(graphs.dijkstra('SKF', weight)['Chalmers']['path'])


import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot'):
    import graphviz as gr
    dot = gr.Graph(name = 'Graph')
    graphs = Graph()
    for v in graphs.vertices():
        dot.node(v)
    edges = graphs.edges()
    for e in range(len(edges)):
        dot.edge(edges[e][0], edges[e][1])
    dot.render(format='png', view=True)
    
def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = Graph.dijkstra(G, source, cost)[target]['path']
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)

def demo():
    G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo()
