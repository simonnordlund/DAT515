import json

TRAM_FILE = './tramnetwork.json'

class Graph():

    def __init__(self): #run verey time class is called to create dictionaries
        with open(TRAM_FILE, 'r', encoding='utf-8') as infile:
            self.data = json.load(infile)
            self.dic_val = {}
            self.dic = {}
            for outer in self.data['times']:
                temp_list = []
                self.dic_val[outer] = []
                for inner in self.data['times'][outer]:
                    temp_list.append(inner)
                self.dic[outer] = temp_list #dictionary of all stops with list nearby stops as value
            
    def neighbours(self, vertex): #find neighbours
        return self.dic[vertex]

    def edges(self): #gives edges
        edges = []
        for key in self.data['times']:
            for key2 in self.data['times'][key]:
                if [key2, key] not in edges and [key, key2] not in edges:
                    edges.append([key, key2])
        return edges

    def vertices(self): #gives all nodes aka stops
        vertices = []
        for key in self.data['stops']:
            vertices.append(key)
        return vertices

    def __len__(self): #amount of stops
        count = len(self.dic)
        return count

    def add_vertex(self, vertex): #adds vertex without neighbours
        if vertex not in self.dic:
            self.dic[vertex] = []
        return self.dic

    def add_edge(self, vertex1, vertex2): #adds edge between two stops
        if vertex1 in self.dic:
            self.dic[vertex1].append(vertex2)
        else:
            self.dic[vertex1] = [vertex2]
        if vertex2 in self.dic:
            self.dic[vertex2].append(vertex1)
        else:
            self.dic[vertex2] = [vertex1]
        return self.dic
    
    def remove_vertex(self, vertex): #removes stop from dictionary
        self.dic.pop(vertex)
        for key in self.dic:
            for i in range(len(self.dic[key])-1):
                if self.dic[key][i]==vertex:
                    self.dic[key].remove(vertex)
        return self.dic

    def remove_edge(self, vertex1, vertex2): #removes edge in dictionary
        self.dic[vertex1].remove(vertex2)
        self.dic[vertex2].remove(vertex1)
        return self.dic

    def get_vertex_value(self, vertex): #gets value
        return self.dic_val[vertex]

    def set_vertex_value(self, vertex, value): #sets value
        if isinstance(vertex, list):
            for i in range(len(vertex)):
                self.dic_val[vertex[i]] = value
        else:
            self.dic[vertex] = value
        return self.dic_val


    class WeightedGraph():

        def __init__(self): #runs every time class called
            with open(TRAM_FILE, 'r', encoding='utf-8') as infile:
                self.data = json.load(infile)
                self.dic_weight = self.data['times']

        def get_weight(self, vertex1, vertex2): #gets weigth between two vertices 
            return self.dic_weight[vertex1][vertex2]

        def set_weight(self, vertex1, vertex2, weight): #sets weight
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

def dijkstra(source, target): #shortest path finding algorithm

    graphs = Graph()
    graphs_weight = Graph.WeightedGraph()
    dist = {} #dictionary of distance between stops
    prev = {} #previous stops, path
    unvisited = [] #list of unvisted stops

    for v in graphs.vertices():
        dist[v] = float('inf') #sets initial distance to inf for all stops

    unvisited = graphs.vertices() #all stops unvisited

    dist[source] = 0 #distance to source 0

    while unvisited != []: #runs while there are unvisted stops

        temp_dist = {}
        for stop in unvisited:
            temp_dist[stop] = dist[stop] #distance for unvisted stops

        min_val = min(temp_dist.values()) #find minimum distance for all unvisited stops
        current = [key for key in temp_dist if temp_dist[key] == min_val] #get key for minimum distance
        current = current[0] #if multiple elements, choose first

        unvisited.remove(current) #current now visited
        neighbour = graphs.neighbours(current) #gets neighbours to current

        for stop in neighbour: #loops over all neighbours
            if stop in unvisited: #unvisted stops
                alt = dist[current] + graphs_weight.get_weight(current, stop) #alternative dist, dist to get to current plus dist to nieghbour
                if alt < dist[stop]: #save shortest dist
                  dist[stop] = alt
                  prev[stop] = current #save path

    S = [] #stop sequence
    u = target #start at target

    if u in prev or u == source: #runs algorithm if path exists       
      while u in prev:   
        S.append(u) #add u to sequence                
        u = prev[u] #go to stop before, algorithm runs backwards
    S.append(source) #add source to sequence                    

    return S

#print(dijkstra('Lana', 'Vårväderstorget'))

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

def visualize():
    import graphviz as gr

    dot = gr.Graph(name = 'Graph')
    graphs = Graph()
    for v in graphs.vertices():
        dot.node(v)
    edges = graphs.edges()
    for e in range(len(edges)):
        dot.edge(edges[e][0], edges[e][1])
    dot.render(format='png', view=True)

'''
def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]['path']
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)

def demo():
    G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo() '''


visualize()


