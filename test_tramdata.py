import unittest
from tramdata import *

TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):
    
            
    def setUp(self):
        with open(TRAM_FILE, encoding='utf-8') as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']
        with open(TRAM_FILE, encoding='utf-8') as textfile: # Added this to read the textfile. Could be moved to the testfunction below.
            self.textfile = textfile.readlines()

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    # add your own tests here ---------------------------------------------------------------

    def test1(self): #A test that verifies that all lines in the original textfile are in the tramnetwork dictionary
        #READS THE DATA
        
        self.list = list(self.linedict.keys())

        with open('tramlines.txt') as f:
            data = f.read()
        b = data.split('\n')
        c =  [list(g) for k, g in groupby(b, key=bool) if k] # splits at empty row, gives list of lists of lines
        dir = []
        for i in range(len(c)):
            dir.append(c[i][0].split(':')[0]) # Stores the line number for each line. 
        assert dir == self.list

    def test2(self): #Test that verifies that all stops in the original textfile are in the tramnetwork dictionary
        #READ THE DATA 
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
        
        with open('tramlines.txt') as f: #Make a list of lists of all stops. 
            data = f.read() 
        b = data.split('\n')
        c = [list(g) for k, g in groupby(b, key=bool) if k] # splits at empty row, gives list of lists of lines
        dirstop = []
        for i in range(len(c)):
            templist = []
            for j in range(1,len(c[i])):
                    templist.append(c[i][j].rsplit(maxsplit = 1)[0]) # splits from right and saves first element, stops
            dirstop.append(templist)
        


        emptylistoflineslist = []
        for linesdict in tramdict["lines"].keys():
            emptylistoflineslist.append(tramdict["lines"][linesdict])
        

        assert dirstop==emptylistoflineslist

    def test3(self):#Test that verifies that the distance between stops don't exceed 20km
        tramstops = build_tram_stops('tramstops.json')

        for stop1 in self.stopdict: 
            for stop2 in self.stopdict:
                assert distance_between_stops(tramstops,stop1,stop2) < 20


    def test4(self): # that the time from a to b is always the same as the time from b to a along the same line.
        self.timelist = list(self.timedict.keys()) #Stores all keys of the times dictionary in a list
        timeval1 = []
        timeval2= []
        for key in self.timedict:
            for boll in self.timedict[key]:
                timeval1.append(self.timedict[key][boll])
                timeval2.append(self.timedict[boll][key])
        assert timeval1 == timeval2 , "Error for times between a and b"

        

                
            

            


            



#that all distances are "feasible", meaning less than 20 km (test this test with a smaller number to see it fail!),





            




#that the list of stops for each tramline is the same in tramlines.txt and linedict
        


if __name__ == '__main__':
    unittest.main()