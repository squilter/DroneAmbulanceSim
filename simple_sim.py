#!/usr/bin/python3
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
with open('data/chosen_firehouses.csv') as firehouse_file:
	reader = csv.reader(firehouse_file, delimiter=',', quotechar=';')
	next(reader)#skip the first line with headers
	for row in reader:
		firehouses.append((float(row[1]),float(row[0])))

distances=[]
emstimes=[]
with open('data/incidents_with_latlongs.csv', 'rU') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar=';')
	next(reader)
	latlon=(0,0)
	for row in reader:
		try:
			if((float(row[15]),float(row[16]))!=latlon):#if this incident has different coords than the previous incident
				latlon=(float(row[15]),float(row[16]))
				distance=find_closest_firehouse(latlon)
				if distance<10000:
					distances.append(distance)
					emstimes.append(float(row[7])*60)
			else:#is incident has same coords, replace ems time if shorter
				if(float(row[7])*60<emstimes[-1]):
					emstimes[-1]=float(row[7])*60					
#print(distance)
		except ValueError:
			continue
			#print(0)
dronetimes=[]
for dist in distances:
	if(dist<3000):
		dronetimes.append(5+30+dist/10)#5sec to calculate/arm,etc. 30 to get to altitude. 10m/sec travel
 


print("Unique: " + str(len(distances)))
print("Mean drone dist: "+ str(statistics.mean(distances)))
print("Median drone dist: "+ str(statistics.median(distances)))
print("stdDev drone dist: "+ str(statistics.pstdev(distances)))
print("")
print("Mean ems time: "+str(statistics.mean(emstimes)))
print("Median ems time: "+str(statistics.median(emstimes)))
print("ems standard deviation: "+str(statistics.pstdev(emstimes)))
print("")
print("Mean drone time: "+str(statistics.mean(dronetimes)))
print("Median drone time: "+str(statistics.median(dronetimes)))
print("drone standard deviation: "+str(statistics.pstdev(dronetimes)))

exit()

