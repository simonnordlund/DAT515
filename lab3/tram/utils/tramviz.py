# visualization of shortest path in Lab 3, modified to work with Django

from .trams import *
from .graphs import *
from .color_tram_svg import color_svg_network
import os
from django.conf import settings

def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code

    # TODO: replace this mock-up with actual computation using dijkstra.
    # First you need to calculate the shortest and quickest paths, by using appropriate
    # cost functions in dijkstra().
    # Then you just need to use the lists of stops returned by dijkstra()
    #
    # If you do Bonus 1, you could also tell which tram lines you use and where changes
    # happen. But since this was not mentioned in lab3.md, it is not compulsory.

    g = readTramNetwork() #network obj, not empty

    cost_time = lambda u,v: g.get_weight(u,v) #cost to travel between two adj stops
    cost_geo = lambda u,v: g.geo_distance(u,v)

    time_path = dijkstra(g, dep, cost_time)

    geo_path = dijkstra(g, dep, cost_geo)

    quickest = time_path[dest]['path']
    quickest.reverse()
    shortest = geo_path[dest]['path']
    shortest.reverse()
    
    timepath = 'Quickest: ' + ', '.join(quickest) + ', 5 minutes'
    geopath = 'Shortest: ' + ', '.join(shortest) + ', 100 km'

    def colors(v):
        if v in shortest and v not in quickest:
            return 'darkseagreen'
        elif v in quickest and v not in shortest:
            return 'orange'
        elif v in quickest and v in shortest:
            return 'darkkhaki'
        else:
            return 'white'
            

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath

