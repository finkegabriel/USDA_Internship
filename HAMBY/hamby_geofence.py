import LatLon2UTM as utm
import serial
import time

#config
portSerial = 'COM4'  # serial communication port, '/dev/ttyACM0' for pi, 'COM#' for others
freqSerial = 9600  # serial communication frequency
ser = None
gps = '$GPGGA'
lat = 0
lon = 0

def configGPS():
	global ser
	while ser is None:
		try:
			ser = serial.Serial(portSerial, freqSerial)
		except serial.serialutil.SerialException:
			print("ERROR: serial communication for port %s at freq %d" %
			      (portSerial, freqSerial))

	print("SUCCESS: serial communication for port %s at freq %d" %
	      (portSerial, freqSerial))

def getLoc(ser):
    global lat,lon
    loc = ser.readline().decode('ascii', errors='replace')
    loc_sp = loc.strip().split(",")
    #print(loc_sp) #uncomment to debug gps
    if loc_sp[0] == gps:
        try:
            #print(loc_sp) 
            lat, lp,lon = (loc_sp[i] for i in range(2,5)) #format available: http://aprs.gids.nl/nmea/#latlong
            lat = int(float(lat[:-8]))+float(lat[-8:])/60
            lon = 0-(int(float(lon[:-8]))+float(lon[-8:])/60) #assumed to be in usa to speed up
        except:
            #print("error")
            return 0,0
    else:
        #print(loc_sp) #uncomment to debug gps
        return 0,0

    return lat,lon


def getGps():
    latLast, lonLast = getLoc(ser)
    if latLast !=0 and lonLast !=0:
        return [latLast,lonLast]
    else:
        return [0,0]


def main():
    configGPS()
    while getGps():
        LatLon = getGps()
        #print(LatLon)
        if LatLon[0] !=0 and  LatLon[1] !=0:
            Lon_deg, Lat_deg, Easting, Northing = utm.Convert_LL2UTM(LatLon)
            print("UTM "+str(Easting)+" "+str(Northing))

main()
