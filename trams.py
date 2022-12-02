
import json
import sys


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









