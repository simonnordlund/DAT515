import graphs as gr
import tramdata as td
import json
import sys
import math


class TramStop():

    def __init__(self, name, lat, lon, lines=[]):
        self._lines = lines
        self._name = name
        self._position = {'lat':lat, 'lon':lon}

    def add_line(self, line):
        self._lines.append(line)
        return self._lines

    def get_lines(self): 
        return self._lines

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position = {'lat':lat, 'lon':lon}
        return self._position

class TramLine():

    def __init__(self, num, stops=[]):
        self._number = str(num)
        self._stops = stops

    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops


class TramNetwork(gr.WeightedGraph):
    
    def __init__(self, stops, lines, times, G = None):
        super(TramNetwork, self).__init__(G) #inherit from Graph

        self._linedic = lines
        self._stopdic = stops
        self._timedic = times


    def all_lines(self): #returns all lines
        keys = []
        for key in self._linedic:
            keys.append(key)
        return keys


    def all_stops(self): #return all stops
        keys = []
        for key in self._stopdic:
            keys.append(key)
        return keys


    def extreme_positions(self): #get extreme lat and lon position

        lat = []
        lon = []

        for stop in self._stopdic: #append all lon lat
            lat.append(float(self._stopdic[stop]['lat']))
            lon.append(float(self._stopdic[stop]['lon']))
        
        lat.sort() #sort lists after value
        lon.sort() #sort lists after value

        max_lat = lat[-1]
        min_lat = lat[0]
        max_lon = lon[-1]
        min_lon = lon[0]

        dic = {'lat': {'max': max_lat, 'min': min_lat}, 'lon': {'max': max_lon, 'min': min_lon}}
        
        return dic


    def geo_distance(self, stop1, stop2):
                
        lat1 = float(self._stopdic[stop1]['lat']) #lat for stop1
        lon1 = float(self._stopdic[stop1]['lon']) #lon for stop1
        lat2 = float(self._stopdic[stop2]['lat']) #lat for stop2
        lon2 = float(self._stopdic[stop2]['lon']) #lon for stop2

        delta_lat = math.abs(lat2-lat1)*(math.pi/180) #difference in lat in radians
        delta_lon = math.abs(lon2-lon1)*(math.pi/180) #difference in lon in radians
        mean_lat = ((lat1+lat2)/2)*(math.pi/180) #mean lat in radians
        radius = 6371 #earth radius in km

        distance = radius*math.sqrt(delta_lat**2 + (math.cos(mean_lat)*delta_lon)**2) #distance assuming spherical earth in km

        return distance


    def line_stops(self, line):
        return self._linedic[line]

    def stop_lines(self, stop):
        lines = []
        for key in self._linedic: #loops over all lines
            if stop in self._linedic[key]: #checks if stop is on line
                lines.append(key)
        return lines

    def stop_positions(self, stop):
        return self._stopdic[stop] #returns dictionary

    def transition_times(self, stop1, stop2):
        return self._stoptime[stop1][stop2] #time between adjacent stops


TRAM_FILE = './tramnetwork.json'

def readTramNetwork(tramfile = TRAM_FILE):

    with open(tramfile, 'r', encoding = 'utf-8') as infile:
        data = json.load(infile)
        stops = data['stops']
        lines = data['lines']
        times = data['times']

        network = TramNetwork(stops, lines, times) #network obj with all graphs and network functions, empty
    
    for stop in stops:
        network.set_vertex_value(stop, stops[stop]) #add vertex value, lat lon
        network.add_vertex(stop) #add vertex as stops

    for stop1 in times:
        for stop2 in times[stop1]:
            network.set_weight(stop1, stop2, times[stop1][stop2]) #set weight as time between stop
            network.add_edge(stop1, stop2) #add edge between adjacent stops

    return network



r = readTramNetwork() #network obj, not empty
cost = lambda u,v: r.get_weight(u,v) #cost to travel between two adj stops

#gr.view_shortest(r, 'Saltholmen', 'Chalmers', cost)

def demo():
        G = readTramNetwork()
        a, b = input('from,to ').split(',')
        gr.view_shortest(G, a, b)

if __name__ == '__main__':
    demo()
