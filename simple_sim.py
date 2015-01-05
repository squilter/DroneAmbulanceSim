#!/bin/python2
import csv
from geopy.distance import vincenty

firehouses=[]
with open('data/FirehouseData.csv') as firehouse_file:
	reader = csv.reader(firehouse_file, delimiter=',', quotechar=';')
	reader.next()#skip the first line with headers
	for row in reader:
		firehouses.append((float(row[0]),float(row[1])))
		
def find_closest_firehouse(incident_coord):
	closest_distance = 99999999999
	closest_firehouse = 0
	for firehouse_coord in firehouses:
		distance = vincenty(firehouse_coord,incident_coord).meters
		if(distance<closest_distance):
			closest_distance=distance
	return closest_distance

with open('data/incidents_with_latlongs.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar=';')
	for row in reader:
		print(find_closest_firehouse(float(row[15]),float(row[16])))

exit()

