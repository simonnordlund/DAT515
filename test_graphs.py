import unittest
from graphs import *
import numpy as np

TRAM_FILE = './tramnetwork.json'

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.G = []
        for i in range(20):
            int1 = np.random.random_integers(1, 10, 1)
            int2 = np.random.random_integers(1, 10, 1)
            if int1 != int2:
                self.G.append((int1[0], int2[0]))
        self.g = Graph(self.G)

    def test1(self):

        vertices = self.g.vertices()
        edges = self.g.edges()

        print(edges, vertices)

        for item in edges:
            self.assertIn(item[0], vertices, msg = 'edge does not exist in vertices')
            self.assertIn(item[1], vertices, msg = 'edge does not exist in vertices')


    def test2(self):

        for a in self.g.vertices():
            neighbours_a = self.g.neighbours(a)
            for b in neighbours_a:
                neighbours_b = self.g.neighbours(b)
                self.assertIn(a, neighbours_b, msg = 'neighbours did not match')

            
    def test3(self):
        import graphs as gr
        for a in self.g.vertices():
            for b in self.g.vertices():
                if a != b:
                    atob = gr.dijkstra(self.g, a, cost=lambda u,v: 1)[b]['path']
                    btoa = gr.dijkstra(self.g, b, cost=lambda u,v: 1)[a]['path']
                    assert atob == btoa[::-1]


if __name__ == '__main__':
    unittest.main()



