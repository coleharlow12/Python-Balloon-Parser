import serial #imports the serial module 
import time #imports the time module

ser = serial.Serial('/dev/tty.usbserial-A906NC0Z', 57600)
time.sleep(2) # pauses for 2 seconds and allows the radio time to start recieving a signal


ser.readline() #This is just used as a precauton to flush out any data on the serial line
ser.readline()
ser.readline()

ser.flushInput() #This is done to really ensure the Serial input is flushed. 

firstSignal = True  #Once we have read the Serial line 3 times and flushed the received data
                    #We can set the firstSignal variable as true. 

while firstSignal:  #This is an infinite while loop used to recieve and store data from the
                    #radio modem

    ser.flushInput() #This flushes out the PySerial Buffer before reading. 
    longitude = ser.readline() # reads the longitude data from serial
    latitude = ser.readline() # reads the latitude data from serial
    altitude = ser.readline() # reads the altitude data from serial
    ser.flushInput() #flushs the serial moniter

    strLongitude = longitude.replace(" ", "")   #When the data is initially read it is in string form
    strLatitude = latitude.replace(" ", "")     #these commands remove the spaces in our strings.

    floatLong = float(strLongitude) #once the spaces are removed we can convert the received strings into 
    floatLat = float(strLatitude)   #float variables

    if not (floatLong == 0) and (not floatLat == 0): #if the recieved values are 0
        firstSignal = False                          #then we have recieved the first long and lat

#END firstSignal Loop_______________________________________________________

lastLong = floatLong    #Sets the last longitude to the most recently read longitude data
lastLat = floatLat      #Sets the last latitude to the most recently read latitude data



f = open('entirePath.kml', 'w') #opens the file to be written in the write mode

#This is the first writing of the file so we have to write additional parameters so that the file is formatted correctly. 
f.write("<?xml version='1.0' encoding='UTF-8'?>\n" #begins writing the KML file line by line in the correct format
"<kml xmlns='http://www.opengis.net/kml/2.2'>\n"
"<Document>\n"
"<Style id='yellowPoly'>\n"
"<LineStyle>\n"
"<color>7f00ffff</color>\n"
"<width>15</width>\n"
"</LineStyle>\n"
"<PolyStyle>\n"
"<color>7f00ff00</color>\n"
"</PolyStyle>\n"
"</Style>\n"
"<Placemark><styleUrl>#yellowPoly</styleUrl>\n"
"<LineString>\n"
"<extrude>1</extrude>\n"
"<tesselate>1</tesselate>\n"
"<altitudeMode>absolute</altitudeMode>\n"
"<coordinates>\n")
f.write("%f,%f,%f " % (float(longitude),float(latitude),float(altitude)))  #This line inputs the first set of coordinates into the KML file
f.write("\n</coordinates>\n"
"</LineString></Placemark>\n\n"
"</Document></kml>")

#Closes the files
f.close()

# creates another file in write mode that displays only the most recent location
f = open('currentLocation.kml', 'w')

f.write("<?xml version='1.0' encoding='UTF-8'?>\n" #begins writing the KML file line by line in the correct format
"<kml xmlns='http://www.opengis.net/kml/2.2'>\n"
"<Document>\n"
"<Style id='yellowPoly'>\n"
"<LineStyle>\n"
"<color>7f00ffff</color>\n"
"<width>15</width>\n"
"</LineStyle>\n"
"<PolyStyle>\n"
"<color>7f00ff00</color>\n"
"</PolyStyle>\n"
"</Style>\n"
"<Placemark><styleUrl>#yellowPoly</styleUrl>\n"
"<LineString>\n"
"<extrude>1</extrude>\n"
"<tesselate>1</tesselate>\n"
"<altitudeMode>absolute</altitudeMode>\n"
"<coordinates> \n")
f.write("%f,%f,%f " % (float(longitude),float(latitude),float(altitude))) 
f.write("\n</coordinates>\n"
"</LineString></Placemark>\n\n"
"</Document></kml>")

f.close() #closes the file

while True: #starts an infinite while loop to update the kml files with new data. 

    longitude = ser.readline() # reads the longitude data from serial
    latitude = ser.readline() # reads the latitude data from serial
    altitude = ser.readline() # reads the altitude data from serial
    
    ser.flushInput() #flushs the serial moniter

    #counts the number of . symbols in the string longitude and latitude each string should have one
    countLong = longitude.count('.') 
    countLat = latitude.count('.')
    countAlt = altitude.count('.')

    #The if checks to ensure that each of the strings has only a single '.'
    if countLong == 1 and countLat == 1 and countAlt == 1 :

        #The .index function returns the index of the specified character within the string.
        indexLong = longitude.index('.')
        indexLat = latitude.index('.')
    
        #next the program counts the number of '-' symbols in each string, there should be at most 1
        countLong = longitude.count('-')
        countLat = latitude.count('-')
        countAlt = altitude.count('-')

        #The program then checks to make sure that there will only be at most 1 '-' and that the decimal point is at most the 4th character in the string. 
        if countLong <= 1 and indexLong <= 4 and countLat <= 1 and indexLat <= 4 and countAlt <= 1:

            #We create these indexes to handle the case in which there is no '-' in either the longitude or latitude data
            indexLong = 0
            indexLat = 0

            #if there is a '-' symbol in the string then the if loops will find its index
            if countLong == 1:
                indexLong = longitude.index('-')

            if countLat == 1:
                indexLat = latitude.index('.')

            #The two indexs must be 0 to show that the '-' symbol is the first in the string of data
            if indexLong == 0 and indexLat == 0 :

                #removes all of the spaces within the latitude and longitude strings
                strLongitude = longitude.replace(" ", "")
                strLatitude = latitude.replace(" ", "")
                s

                #converts the longitude and latitude into a float variable for one final test
                floatLong = float(strLongitude)
                floatLat= float(strLatitude)

                changeLong = floatLong - lastLong #calculates the changes in latitude and longitude
                changeLat = floatLat - lastLat

                # makes sure that the latitude and longitude have changed by reasonable values
                if changeLong > -1 and changeLong < 1 and changeLat > -1 and changeLat < 1 and not (lastLong == floatLong) and not (lastLat == floatLat): #ensures that the longitude and latitude have changed only reasonable amounts also meant to stop corrupted data                               
                    f = open('entirePath.kml','r+') #opens the file entirePath.kml in the read/write mode
                    f.seek(-59,2) #finds the 59th character before the end of the file. This is where we want to insert new data
                    f.write("%f,%f,%f " % (floatLong,floatLat,float(altitude))) #inserts the new data with the correct formatting
                    f.write("\n</coordinates>\n" #rewrites the files ending lines
                    "</LineString></Placemark>\n\n" #note there are 59 characters (not including the first newline character)
                    "</Document></kml>")

                    f.close() #closes the entire path kml file

                    f = open ('currentLocation.kml','r+') #opens the current location kml file. 
                    f.seek(-92,2) #finds the point 92 characters before the end note it is 92 because we have to overwrite the previous data
                    f.write("%f,%f,%f " % (float(longitude),float(latitude),float(altitude))) #inserts the new data
                    f.write("\n</coordinates>\n" #writes the end of the file
                    "</LineString></Placemark>\n\n"
                    "</Document></kml>")

                    f.close() #closes the file
                
                    lastLong=floatLong #replaces the lastLong with the most recent values
                    lastLat=floatLat   #replaces the lastLat with the most recent latitude. 
