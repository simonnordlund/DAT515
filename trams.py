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
    
    def __init__(self):
        super(TramNetwork, self).__init__(G)
        #with open('tramnetwork.json', 'r') as infile:
            #tramdict = json.load(infile)

        self._linedic = {}
        self._stopdic = {}
        self._timedic = {}

            #self._linedic = tramdict['lines']
            #self._timedic = tramdict['times']
            #self._stopdic = tramdict['stops']

    def all_lines(self):
        return self._linedic.keys

    def all_stops(self):
        return self._stopdic.keys

    def extreme_positions(self):

        maxval_lat = 0
        minval_lat = float('inf')

        maxval_lon = 0
        minval_lon = float('inf')

        for key in self._stopdic: 

            lat_val = float(self._stopdic[key]['lat'])
            lon_val = float(self._stopdic[key]['lon'])

            #finding max min lat
            if lat_val> maxval_lat:
                maxval_lat = lat_val

            elif lat_val < minval_lat:
                minval_lat = lat_val

            #finding max and min lon
            if lon_val> maxval_lon:
                maxval_lon = lon_val

            elif lon_val< minval_lon:
                minval_lon = lon_val

        dic = {'lat': {'max': maxval_lat, 'min': minval_lat}, 'lon': {'max': maxval_lon, 'min': minval_lon}}
        
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
        return self._stoptime[stop1][stop2]


TRAM_FILE = './tramnetwork.json'

def ReadTramNetwork(tramfile = TRAM_FILE):
    network = TramNetwork()
    stopdic







