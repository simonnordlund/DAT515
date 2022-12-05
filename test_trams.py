from collections import deque

import unittest
from tramdata import *
import trams as ts
import graphs as gs
TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):
    
            
    def setUp(self):
        self.tn = ts.ReadTramNetwork()


    def BFS(self ,G, node, goal = lambda n : False):
        Q = deque() 
        explored = [node]
        Q.append(node)
        while Q:
            v = Q.popleft()
            if goal(v):
                return v
            for w in G.neighbours(v):
                if w not in explored:
                    explored.append(w)
                    Q.append(w)
        return explored

    def testbreathsearch(self): #Tests that our graph is connected.
        for stop in self.tn.vertices():
            #print(stop)
            testlist = self.BFS(self.tn, stop, goal = lambda n : False)
            self.assertTrue(sorted(testlist), sorted(self.tn.vertices()))

def demo():
    G = ts.ReadTramNetwork()
    a, b = input('from,to ').split(',')
    gs.view_shortest(G, a, b)

    
demo()


if __name__ == '__main__':
    unittest.main()
    demo()





        