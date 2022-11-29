import json

TRAM_FILE = './tramnetwork.json'

class Graph():

    def __init__(self):
        with open(TRAM_FILE, 'r', encoding='utf-8') as infile:
            self.data = json.load(infile)
            self.dic_val = {}
            self.dic = {}
            for outer in self.data['times']:
                temp_list = []
                self.dic_val[outer] = []
                for inner in self.data['times'][outer]:
                    temp_list.append(inner)
                self.dic[outer] = temp_list
            
    def neighbours(self, vertex):
        return self.dic[vertex]

    def edges(self):
        edges = []
        for key in self.data['times']:
            for key2 in self.data['times'][key]:
                if [key2, key] not in edges and [key, key2] not in edges:
                    edges.append([key, key2])
        return edges

    def vertices(self):
        vertices = []
        for key in self.data['stops']:
            vertices.append(key)
        return vertices

    def __len__(self):
        count = len(self.dic)
        return count

    def add_vertex(self, vertex):
        if vertex not in self.dic:
            self.dic[vertex] = []
        return self.dic

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.dic:
            self.dic[vertex1].append(vertex2)
        else:
            self.dic[vertex1] = [vertex2]
        if vertex2 in self.dic:
            self.dic[vertex2].append(vertex1)
        else:
            self.dic[vertex2] = [vertex1]
        return self.dic
    
    def remove_vertex(self, vertex):
        self.dic.pop(vertex)
        for key in self.dic:
            for i in range(len(self.dic[key])-1):
                if self.dic[key][i]==vertex:
                    self.dic[key].remove(vertex)
        return self.dic

    def remove_edge(self, vertex1, vertex2):
        self.dic[vertex1].remove(vertex2)
        self.dic[vertex2].remove(vertex1)
        return self.dic

    def get_vertex_value(self, vertex):
        return self.dic_val[vertex]

    def set_vertex_value(self, vertex, value):
        if isinstance(vertex, list):
            for i in range(len(vertex)):
                self.dic_val[vertex[i]] = value
        else:
            self.dic[vertex] = value
        return self.dic_val


    class WeightedGraph():

        def __init__(self):
            with open(TRAM_FILE, 'r', encoding='utf-8') as infile:
                self.data = json.load(infile)
                self.dic_weight = self.data['times']

        def get_weight(self, vertex1, vertex2):
            return self.dic_weight[vertex1][vertex2]

        def set_weight(self, vertex1, vertex2, weight):
            self.dic_weight[vertex1][vertex2] = weight
            self.dic_weight[vertex2][vertex1] = weight
            return self.dic_weight

graphs = Graph()
graph_weight = Graph.WeightedGraph()
'''
def djikstra(graph, source):

    with open(graph, 'r', encoding='utf-8') as infile:
        graphs = Graph()
        data = json.load(infile)
        unvisited = list(data['times'].keys())
        tent_dist = graphs.set_vertex_value(unvisited, float('inf'))
        tent_dist[source] = 0
        tent_dist_temp = tent_dist
        current = source

        while unvisited != []:
            for i in range(len(graphs.neighbours(current))): #loops over all nieghbours to current
                if graphs.neighbours(current)[i] in unvisited: #checks if neighbour unvisited
                    neighbour = graphs.neighbours(current)[i]
                    weight = tent_dist[current] + data['times'][current][neighbour] #weight for nieghbour + weight current
                    if weight < tent_dist[neighbour]: #if weight smaller than tentative dist
                        tent_dist[neighbour] = weight #set new tent dist to weigth
                        tent_dist_temp[neighbour] = weight
            unvisited.remove(current) #current visited so remove
            tent_dist_temp.pop(current)
            current = min(tent_dist_temp)
            #print(current)
    return tent_dist

print(djikstra('tramnetwork.json', 'Chalmers')) '''

def dijkstra(source, target):

    graphs = Graph()
    graphs_weight = Graph.WeightedGraph()
    dist = {}
    prev = {}
    unvisited = []

    for v in graphs.vertices():
        dist[v] = float('inf')

    unvisited = graphs.vertices()

    dist[source] = 0

    while unvisited != []:

        temp_dist = {}
        for stop in unvisited:
            temp_dist[stop] = dist[stop]

        min_val = min(temp_dist.values())
        current = [key for key in temp_dist if temp_dist[key] == min_val]
        current = current[0]

        unvisited.remove(current)
        neighbour = graphs.neighbours(current)

        for i in range(len(neighbour)):
            if neighbour[i] in unvisited:
                alt = dist[current] + graphs_weight.get_weight(current, neighbour[i])
                if alt < dist[neighbour[i]]:
                  dist[neighbour[i]] = alt
                  prev[neighbour[i]] = current

    S = []
    u = target
    if u in prev or u == source:          
      while u in prev:   
        S.append(u)                   
        u = prev[u]  
    S.append(source)                     

    return S

print(dijkstra('Chalmers', 'Långedrag'))










        


