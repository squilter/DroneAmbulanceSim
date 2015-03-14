#!/usr/bin/python3
import csv

from http.server import BaseHTTPRequestHandler, HTTPServer
from geopy.distance import vincenty

hostName = "localhost"
hostPort = 80

def find_closest_firehouse(incident_coord):
        closest_distance = 99999999999
        closest_firehouse = 0
        for firehouse_coord in firehouses:
                distance = vincenty(firehouse_coord,incident_coord).meters
                if(distance<closest_distance):
                        closest_distance=distance
        return closest_distance

def convert_meters_to_drone_time(dist):
	return(5+30+dist/10)

def handle_latlon(path):
	(lat_s,lon_s)=path[1:].split(",",1)
	(lat,lon)=(float(lat_s),float(lon_s))
	print(lat)
	print(lon)
	print("closest firehouse: ",find_closest_firehouse((lat,lon)))	
	print("drone time: ",convert_meters_to_drone_time(find_closest_firehouse((lat,lon))))	

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		handle_latlon(self.path)
		self.wfile.write(bytes("<html><body><p>seb</p></body></html>","utf-8"))

#preload firehouses
firehouses=[]
with open('../data/chosen_firehouses.csv') as firehouse_file:
        reader = csv.reader(firehouse_file, delimiter=',', quotechar=';')
        next(reader)#skip the first line with headers
        for row in reader:
                firehouses.append((float(row[1]),float(row[0])))
myServer = HTTPServer((hostName,hostPort), MyServer)

print("Server Started")

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print("Server Stopped")
