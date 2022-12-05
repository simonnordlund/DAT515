import json
from itertools import groupby
import math
import sys

def build_tram_stops(jsonobject='tramstops.json'):

    with open(jsonobject, 'r') as infile:
        data = json.load(infile)
        dic = {}
        for key in data:
            dicpos = {'lat':data[key]['position'][0], 'lon':data[key]['position'][1]} # inner dictionary for positions, ignores city
            dic[key] = dicpos #key=stop names, outer dictionary with stop names as keys and dicpos as values
    return(dic)





def build_tram_lines(lines='tramlines.txt'):

    with open(lines, encoding='utf-8') as f:
        data = f.read()
        data2 = data.split('\n')
        data3 = [list(g) for k, g in groupby(data2, key=bool) if k] #splits at empty row, gives list of lists of lines
        dic = {}
        for i in range(len(data3)):
            dicstop = []
            for j in range(1,len(data3[i])):
                dicstop.append(data3[i][j].rsplit(maxsplit = 1)[0]) #splits from right and saves first element, stops
            dic[data3[i][0].split(':')[0]] = dicstop #dictionary of stops with lines as keys
    return(dic)


def build_tram_times(lines='tramlines.txt'):

    with open(lines, encoding='utf-8') as f:
        data = f.read()
        data = data.split('\n')
        data = [list(g) for k, g in groupby(data, key=bool) if k] #list of lists, where every element is a line
        dictime = {} #empty dictionary
        outer = {} #empty dictionary
        timelist = [] #empty list
        stoplist = [] #empty list

        for i in range(len(data)):

            time = []
            stop = []

            for j in range(1,len(data[i])):

                min = (data[i][j].rsplit(maxsplit = 1)[1]) #splits from right at first space, saves second element, time
                min = int(min.split(':')[1]) #splits each time into two, saves minutes
                stop.append(data[i][j].rsplit(maxsplit = 1)[0]) #append stops to list
                time.append(min) #append time to list

            timelist.append(time+time[-2::-1]) #list of lists of time
            stoplist.append(stop+stop[-2::-1]) #list of lists of stop

        
        for i in range(len(stoplist)): #loops over lines
            for j in range(0,len(stoplist[i])-1): #loops over stops for each line

                inner={}
                inner[stoplist[i][j+1]] = abs(timelist[i][j+1]-timelist[i][j]) #inner dictionary, time between two near stops

                if stoplist[i][j] in outer and stoplist[i][j+1] in outer[stoplist[i][j]]: #already exists in dictionary
                    pass

                elif stoplist[i][j] not in outer: #not key in outer, so add with inner as value
                    outer[stoplist[i][j]] = inner 

                elif stoplist[i][j] in outer and stoplist[i][j+1] not in outer[stoplist[i][j]]: #inner not value, update keys value
                    outer[stoplist[i][j]].update(inner) #adds new stop to inner dictionary
        return outer



def build_tram_network(): #Creates a concatenated dictionary of all functions.
    stops=build_tram_stops()

    lines=build_tram_lines()

    times=build_tram_times()

    dict = {"stops": stops, "lines": lines, "times": times}
    file = open("tramnetwork.json", "w", encoding='utf-8')#opens file tramnetwork.json
    #dump dict to file, 
    json.dump(dict, file, indent=4, separators=None, ensure_ascii=False)
    file.close()#close file
    
#build_tram_network("tramstops.json","tramlines.txt")



#Query functions

def lines_via_stop(tramlines, stop): #checks which lines go through given stop

    lines = []
    for key in tramlines: #loops over all lines
        if stop in tramlines[key]: #checks if stop is on line
            lines.append(key)
    return lines



def lines_between_stops(tramlines, stop1, stop2): #checks which lines go through two given stops
    
    lines = []
    for key in tramlines: #loops over all lines
        if stop1 in tramlines[key] and stop2 in tramlines[key]: #checks if both stops are on the line
            lines.append(key)
    return lines


def time_between_stops(tramlines, tramtimes, line, stop1, stop2): #checks time between two stops given specific line

    time = 0

    if stop1 in tramlines[line] and stop2 in tramlines[line]: #check if stops both on the given line

        index1 = tramlines[line].index(stop1)
        index2 = tramlines[line].index(stop2)

        if index1 < index2: #then we travel the given direction
            for i in range(index1, index2):
                time = time + tramtimes[tramlines[line][i]][tramlines[line][i+1]] #sums time between stops from time dictionary

        elif index1 > index2: #we travel opposite to the given direction
            for i in range(index2, index1):
     
                time = time + tramtimes[tramlines[line][i]][tramlines[line][i+1]] #sums time between stops from time dictionary

    else:
        print('Stops are not on the same line.')

    return time



def distance_between_stops(tramstops, stop1, stop2): #calculates geographical distance between two stops

    lat1 = float(tramstops[stop1]['lat']) #lat for stop1
    lon1 = float(tramstops[stop1]['lon']) #lon for stop1
    lat2 = float(tramstops[stop2]['lat']) #lat for stop2
    lon2 = float(tramstops[stop2]['lon']) #lon for stop2

    delta_lat = math.abs(lat1-lat2)*math.pi/180 #difference in lat in radians
    delta_lon = math.abs(lon1-lon2)*math.pi/180 #difference in lon in radians
    mean_lat = ((lat1+lat2)/2)*math.pi/180 #mean lat in radians
    radius = 6371 #earth radius in km

    dist = radius*math.sqrt((delta_lat)**2 + (math.cos(mean_lat)*delta_lon)**2) #distance assuming spherical earth in km
    
    return dist


def answer_query(tramdict, query):
    #READ THE DATA
    tramlines = tramdict['lines']
    tramtimes = tramdict['times']
    tramstops = tramdict['stops']
    query = query.split(maxsplit = 1)

    while query[0] != 'quit': #Loops until given "quit"

        if query[0] == 'via':
            print(lines_via_stop(tramlines, query[1]))

        elif query[0] == 'between':
            stop1 = query[1].split('and')[0] 
            stop2 = query[1].split('and')[1]
            stop1 = stop1[:-1]
            stop2 = stop2[1:]
            
            if stop1 in tramstops and stop2 in tramstops:
                print(lines_between_stops(tramlines, stop1, stop2))
            else:
                print('Unknown arguments.')

        elif query[0] == 'time':
            stop2 = query[1].split('to')[1]
            stop1 = (query[1].split('to')[0]).split('from')[1]
            stop1 = stop1[1:-1]
            stop2 = stop2[1:]
            line = ((query[1].split('to')[0]).split('from')[0]).split()[1]

            if stop1 in tramstops and stop2 in tramstops and line in tramlines:
                print(time_between_stops(tramlines, tramtimes, line, stop1, stop2))

            else:
                print('Unknown arguments.')

        elif query[0] == 'distance':
            stop2 = query[1].split('to')[1]
            stop1 = (query[1].split('to')[0]).split('from')[1]
            stop1 = stop1[1:-1]
            stop2 = stop2[1:]

            if stop1 in tramstops and stop2 in tramstops:
                print(distance_between_stops(tramstops, stop1, stop2))

            else:
                print('Unknown arguments.')

        else:
            print('Sorry, try again.')

        query = input('> ') #Repeats input
        query = query.split(maxsplit = 1) #Check first word acknowledge which function to use

    return


def dialogue(jsonfile='tramnetwork.json'):
    #Open file and stores in variables 
    with open(jsonfile, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
        inp = input('> ')
        ans = answer_query(data, inp)

    return ans



if __name__ == '__main__': #This code was given
    if sys.argv[1:] == ['init']:
        build_tram_network()
    else:
        dialogue()	

