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
        self.dic_val[vertex] = value
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

            
    def dijkstra(graph, source, cost=lambda u,v: 1):



graph = Graph()
graph2 = Graph.WeightedGraph()

print(graph2.set_weight("Chalmers", "Korsvägen", 7))
