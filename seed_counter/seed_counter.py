import serial 
import os
from datetime import datetime
import csv
import sys
import time
import subprocess

ser = serial.Serial('/dev/ttyUSB0',9600,timeout = .4) #connect barcode scanner
scale = serial.Serial('/dev/ttyACM0',57600) #connect scale
#20200921_104125_dfcode
lastCode=["",""]

def cameraConfig(expo,iso):
	#this function will be able to set the camera settings, iso, and exposoure
	print("ISO")	
	x = "gphoto2 \
    --set-config shutterspeed=%s \
    --set-config iso=%s" %(expo,iso)
	print(x)
	os.system(x)

def toggleCode(lastCode):
	if lastCode[0] != lastCode[1]:
		print("newCode")
		return True
	else:
		print("oldCode")
		return False

def exportToCsv(data,barcode,scale):
	print("csv")
	# field names
	csvresult = open("results.csv","a")
	csvresult.write(data+","+scale+","+barcode+"\n") #+","+scale+"\n")
	#int increment, barcode, weight scale, img anay
	csvresult.close

def trigger(ser):
    s = ser.readline() 
    print(s)
    if s != '': #if we read a code then trigger camera and sensor
	lastCode[0]=s
	if toggleCode(lastCode) != False:
		lastCode[1]=s
		print(lastCode)
       		print("CANNON CAMERA","SCALE")
       		print("barcode "+s)
       		cameraConfig("7",300)
       		filename = ("%s"%(datetime.now().strftime("%Y%m%d_%H%M%S")))
#       		scaleRead = scale.readline()
 #      		time.sleep(3)
       		os.system("mkdir %s" %(datetime.now().strftime("%Y%m%d")))       
       #print(scaleRead)
      		list = os.listdir(datetime.now().strftime("%Y%m%d")+"/")
      		num_files = len(list)
       		print(num_files)
       		x = "gphoto2 --capture-image-and-download --filename "'%s/%s_%s.jpg'"" %(datetime.now().strftime("%Y%m%d"),filename,s) #triggers the camera
       #print(x) #uncomment to debug
       		time.sleep(3)
       		os.system(x)
       		list2 = os.listdir(datetime.now().strftime("%Y%m%d")+"/")
       		num_files2 = len(list2)
	       	if num_files2 > num_files: #checking if it took a picture or not
			scaleRead = scale.readline()  
#			print(scaleRead)
			time.sleep(3)
			print(scaleRead)
     			exportToCsv(filename,s,scaleRead) #,scaleRead) #,scaleRead) #if it took a picture without an error then we export the data to a csv
	       		#print("length "+str(num_files2)) #uncomment to debug
	else:
		print("same code")

def readBarCode(ser):
    while True: #create a loop to read barcodes   
	trigger(ser)
	
def main():
    print("seed counter v1")
    readBarCode(ser)

main()
