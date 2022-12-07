import json

# imports added in Lab3 version
import math
import os
from .graphs import *
from django.conf import settings


# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here

TRAM_FILE = './tramnetwork.json'


# TODO: use your lab 2 class definition, but add one method
# class TramNetwork(WeightedGraph):    
    # def extreme_positions(self):
        # stops = self._stopdict.values()
        # minlat = min([s._position[0] for s in stops])
        # etc
        # return minlon, minlat, maxlon, maxlat


class TramNetwork(WeightedGraph):
    
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

        delta_lat = abs(lat2-lat1)*(math.pi/180) #difference in lat in radians
        delta_lon = abs(lon2-lon1)*(math.pi/180) #difference in lon in radians
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




def readTramNetwork():

    with open(TRAM_FILE, 'r', encoding = 'utf-8') as infile:
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




# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance


