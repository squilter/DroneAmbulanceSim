#!/bin/python3
import csv
import statistics

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
	next(reader)#skip the first line with headers
	for row in reader:
		firehouses.append((float(row[1]),float(row[0])))

distances=[]
with open('data/incidents_with_latlongs.csv', 'rU') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar=';')
	next(reader)
	latlon=(0,0)
	for row in reader:
		try:
			if((float(row[15]),float(row[16]))!=latlon):
				latlon=(float(row[15]),float(row[16]))
				distance=find_closest_firehouse(latlon)
				if distance<10000:
					distances.append(distance)
					#print(distance)
		except ValueError:
			continue
			#print(0)
print("Unique: " + str(len(distances)))
print("Min: "+ str(min(distances)))
print("Max: "+ str(max(distances)))
print("Mean: "+ str(statistics.mean(distances)))
print("Median: "+ str(statistics.median(distances)))
print("stdDev: "+ str(statistics.pstdev(distances)))

exit()

