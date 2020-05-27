import time
import serial
import gmplot 
import sys
from datetime import datetime

file_name = sys.argv[1] + ".csv"

lat_list = []
lng_list = []

# Initialize the Google Maps plotter
gmap1 = gmplot.GoogleMapPlotter(34.14180996, -118.2253155, 13 ) 
gmap1.apikey = "API KEY"

def readString():
    '''Read line of coordinate data.'''
    while 1:
            while ser.read().decode("utf-8") != '$':
                pass
            line = ser.readline().decode("utf-8")
            return line
        
def getTime(string, format, returnFormat):
    '''Returns time in specified format.'''
    return time.strftime(returnFormat, time.strptime(string, format))
    
def getLatLng(latString, lngString):
    '''Formats the longitude and latitude data to write into file.'''
    try:
        lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1 / 60).lstrip("0.")
        lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1 / 60).lstrip("0.")
        return lat, lng
    except:
        print("")
    
def printGLL(lines):
    '''Prints the coordinate data to the console'''
    try:
        print("========================================GLL========================================")
        latlng = getLatLng(lines[1], lines[3])
        print("Lat: ", latlng[0], lines[2], ", ", "Long: ", latlng[1], lines[4], sep='')
        print("Fix taken at:", getTime(lines[5], "%H%M%S.%f", "%H:%M:%S"), "UTC")
        return
    except:
        print("")
                
def checksum(line): 

    checkString = line.partition("*") 
    checksum = 0 
    for c in checkString[0]: 
        checksum ^= ord(c) 

    try:  # Just to make sure 
        inputChecksum = int(checkString[2].rstrip(), 16) 

    except: 
        print("Error in string") 
        return False 

    if checksum == inputChecksum: 
        return True 

    else: 
        print("=====================================================================================") 
        print("===================================Checksum error!===================================") 
        print("=====================================================================================") 
        print(hex(checksum), "!=", hex(inputChecksum)) 
        return False 

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    try: 
        while True: 
            file = open(file_name, "a")
            line = readString() 
            lines = line.split(",")
        
            if checksum(line):
        
                if lines[0] == "GPGLL": 
    	    
                    try:
                        printGLL(lines)
                        latlng = getLatLng(lines[1], lines[3])
                        newLat = float(latlng[0])
                        newLng = float(latlng[1])
                        newLat *= -1 if lines[2] == 'S' else 1
                        newLng *= -1 if lines[4] == 'W' else 1
                        file.write("\n" + str(getTime(lines[5], "%H%M%S.%f", "%H:%M:%S"))+ "," + str(newLat) + "," + str(newLng))
                        lat_list.append(newLat)
                        lng_list.append(newLng)
                        gmap1.scatter(lat_list, lng_list, '#FF0000',size = 10, marker = False)
                        gmap1.plot(lat_list, lng_list, 'cornflowerblue', edge_width = 1)
                        gmap1.draw("newTest1.html")

                    except:
                        file.write(str(datetime.now()) + '\n')
                        print("")
                else:
                   print("")
                   
            file.close() 

    except: 
        print('Exiting Script')
   



