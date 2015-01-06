#!/bin/python2
import csv
from geopy.distance import vincenty

		
def find_closest_firehouse(incident_coord):
	closest_distance = 99999999999
	closest_firehouse = 0
	for firehouse_coord in firehouses:
		distance = vincenty(firehouse_coord,incident_coord).meters
		if(distance<closest_distance):
			closest_distance=distance
	return closest_distance

firehouses=[]
with open('data/FirehouseData.csv') as firehouse_file:
	reader = csv.reader(firehouse_file, delimiter=',', quotechar=';')
	reader.next()#skip the first line with headers
	for row in reader:
		firehouses.append((float(row[1]),float(row[0])))

with open('data/incidents_with_latlongs.csv', 'rU') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar=';')
	reader.next()
	latlon=(0,0)
	for row in reader:
		try:
			if((float(row[15]),float(row[16]))!=latlon):
				latlon=(float(row[15]),float(row[16]))
				print(find_closest_firehouse(latlon))
		except ValueError:
			print(0)
exit()

