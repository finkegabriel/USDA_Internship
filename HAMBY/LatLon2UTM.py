from math import *

#GPS convertion from Lat\Lon to UTM
def Convert_LL2UTM(LL, CRS=None):  
    #print('LL(%d)='%(len(LL)),LL)
    #Convert Lat\Lon to Lat_deg\Lon_deg        
    if len(LL)>2:   #format of 123,N,456,W            
        Lat = float(LL[0]) 
        Lon = float(LL[2])
        #print (abs(Lat),abs(Lon))
        if abs(Lat)>180:    #if in minutes, min => deg
            Lat_deg =  (Lat//100)+(Lat/100-(Lat//100))*100/60
            Lon_deg =  (Lon//100)+(Lon/100-(Lon//100))*100/60                                           
        if LL[1]=="S": Lat_deg = -Lat_deg
        if LL[3]=="W": Lon_deg = -Lon_deg                                    
    else:
        Lat_deg = float(LL[0]) 
        Lon_deg = float(LL[1])                        

    # convert LL to UTM    
    zone = 1+int((Lon_deg+180)/6)  #UTM Zone, 12=AZ
    if CRS==None:   # default CRS = WGS84
        # Datum WGS84 parameters 
        a = 6378137 #equatorial radius
        f = 1/298.257223563 #flattening
        k0 = 0.9996 #scale factor
        ee = 0.00669438 #eccentricity
        EE = 0.006739497
        LongOrgRad = radians((zone-1)*6-180+3)
        Lat_rad = Lat_deg*pi/180
        Lon_rad = Lon_deg*pi/180
        N = a/sqrt(1-ee*sin(Lat_rad)**2)
        T = tan(Lat_rad)**2
        C = EE*cos(Lat_rad)**2
        A = cos(Lat_rad)*(Lon_rad-LongOrgRad)
        M = a*((1-ee/4-3*ee**2/64-5*ee**3/256)*Lat_rad-(3*ee/8+3*ee**2/32+45*ee**3/1024)*sin(2*Lat_rad)+(15*ee**2/256+45*ee**3/1024)*sin(4*Lat_rad)-(35*ee**3/3072)*sin(6*Lat_rad))    
        #print (LongOrgRad,Lat_rad,Lon_rad,N,T,C,A,M)
        Northing = k0*(M+N*tan(Lat_rad)*(A**2/2+(5-T+9*C+4*C**2)*A**4/24+(61-58*T+T**2+600*C-330*EE)*A**6/720))
        Easting = k0*N*(A+(1-T+C)*A**3/6+(5-18*T+T**2+72*C-58*EE)*A**5/120)+500000  
    else:   #convert LL2UTM using gdal
        if Lat_deg > 0: Is_Northern = 1
        else:           Is_Northern = 0  
        UTM = osr.SpatialReference()    
        UTM.SetWellKnownGeogCS(CRS)   #set coord sys to handle lat/lon  
        UTM.SetUTM(zone, Is_Northern)        
        LL = UTM.CloneGeogCS() #clone only the coord sys      
        LL2UTM = osr.CoordinateTransformation(LL, UTM)  #create transform component    
        Easting,Northing,Altitude = LL2UTM.TransformPoint(Lon_deg, Lat_deg, 0)    
 
    return Lon_deg,Lat_deg,Easting,Northing

def main():        
    LatLon = [33.08002845, -111.9789222]
    Lon_deg,Lat_deg,Easting,Northing = Convert_LL2UTM(LatLon)
    print(Lat_deg,Lon_deg,'N=',Northing,'E=',Easting)
    
if __name__ == '__main__':
    main()