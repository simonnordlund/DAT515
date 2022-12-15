
from trams import *
from graphs import *

dep = 'Chalmers'
dest = 'SKF'

TRAM_FILE = 'tramnetwork.json'


def specialize_stops_to_lines():

    with open(TRAM_FILE, 'r', encoding = 'utf-8') as infile:
        data = json.load(infile)
        stops = data['stops']
        lines = data['lines']
        times = data['times']

        network = TramNetwork(stops, lines, times) #network obj with all graphs and network functions, empty
    
    for stop in stops:
        for line in lines:
            network.set_vertex_value((stop,line), stops[stop]) #add vertex value, lat lon
            if stop in line:
                network.add_vertex((stop, line)) #add vertex as stops

    for stop1 in times:
        for stop2 in times[stop1]:
            for line in lines:
                if stop1 in lines[line] and stop2 in lines[line]:
                    network.add_edge((stop1, line), (stop2, line)) #add edge between adjacent stops
                    network.set_weight((stop1, line), (stop2, line), times[stop1][stop2])

    for stop in stops:
        lines_for_stop = network.stop_lines(stop)
        for line1 in lines_for_stop:
            for line2 in lines_for_stop:
                if line1 != line2:
                    network.add_edge((stop, line1), (stop, line2)) #add edge between adjacent stops
                    network.set_weight((stop, line1), (stop, line2), 5)

    return network

g = specialize_stops_to_lines() #network obj, not empty

cost_time = lambda u,v: g.get_weight(u,v) #cost to travel between two adj stops
cost_geo = lambda u,v: g.geo_distance(u[0],v[0])

time_path = dijkstra(g, dep, cost_time)
geo_path = dijkstra(g, dep, cost_geo)

time = {}
dist = {}
quickest = {}
shortest = {}

line_dep =  g.stop_lines(dep)
line_dest = g.stop_lines(dest)

for l_dep in line_dep:
    time_path = dijkstra(g, (dep, l_dep), cost_time)
    geo_path = dijkstra(g, (dep, l_dep), cost_geo)

    for l_dest in line_dest:
        quickest[((dep, l_dep),(dest, l_dest))] = time_path[(dest, l_dest)]['path']
        shortest[((dep, l_dep),(dest, l_dest))] = geo_path[(dest, l_dest)]['path']

        with open(TRAM_FILE, 'r', encoding = 'utf-8') as infile:
            times = json.load(infile)['times']
            pot_quick = quickest[((dep, l_dep),(dest, l_dest))]

            print(pot_quick)

            for j in range(len(pot_quick)):
                time[((dep, l_dep),(dest, l_dest))] += times[pot_quick[j]][pot_quick[j]]

        for k in range(len(shortest[((dep, l_dep),(dest, l_dest))])-1):
            dist[((dep, l_dep),(dest, l_dest))] += g.geo_distance(shortest[k][0], shortest[k+1][0])

quickest_key = min(time, key=time.get)
shortest_key = min(dist, key=dist.get)

quickest_path = time_path[quickest_key[1]]['path']
shortest_path = geo_path[shortest_key[1]]['path']