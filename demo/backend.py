#!/usr/bin/python3
import csv

from http.server import BaseHTTPRequestHandler, HTTPServer
from geopy.distance import vincenty

hostName = ""
hostPort = 81

def find_closest_firehouse(incident_coord):
        closest_distance = 99999999999
        closest_firehouse = 0
        for firehouse_coord in firehouses:
                distance = vincenty(firehouse_coord,incident_coord).meters
                if(distance<closest_distance):
                        closest_distance=distance
        return closest_distance

def convert_meters_to_drone_time(dist):
        return((5+30+dist/10)/60)

def generate_response(path):
        response = "<H3>Drone Response Time: "
        (lat_s,lon_s)=path[1:].split(",",1)
        (lat,lon)=(float(lat_s),float(lon_s))
        drone_dist = find_closest_firehouse((lat,lon))	
        if(drone_dist<3000):
                response += str(round(convert_meters_to_drone_time(drone_dist),2))	
                response += "mins."
        else:
                response += "N/A"
        response += "</H3><p />"

        response += "<table><col width=\"80\"><col width=\"80\"><col width=\"80\"><tr><td><b>Vehicle</b></td><td><b>Response<br />Time (min)</b></td><td><b>Date</b></td></tr>"
        for incident in incidents:
                if(abs(lat-incident[0])>0.002):# if lat/lon are very different, don't bother caltulating actual dist
                        continue
                if(abs(lon-incident[1])>0.002):
                        continue
                dist=vincenty((lat,lon),(incident[0],incident[1])).meters
                if(dist<=150):
                        response += "<tr>"
                        response += "<td>"+str(incident[3])+"</td>"#vehicle type
                        response += "<td>"+str(round(incident[2],2))+"</td>"#response time
                        response += "<td>"+str(incident[4])+"</td>"#date
                        response += "</tr>"
        response += "</table>"
        return response

class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.send_header('Access-Control-Allow-Origin', '*')                
                self.end_headers()
                html_response = bytes(generate_response(self.path),"utf-8")
                self.wfile.write(html_response)
        def do_OPTIONS(self):
                self.send_response(200, "ok")       
                self.send_header('Access-Control-Allow-Origin', '*')                
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'access-control-allow-origin, accept')  
                self.end_headers()

#preload firehouses
firehouses=[]
with open('../data/chosen_firehouses.csv') as firehouse_file:
        reader = csv.reader(firehouse_file, delimiter=',', quotechar=';')
        next(reader)#skip the first line with headers
        for row in reader:
                firehouses.append((float(row[1]),float(row[0])))

#preload incident data
incidents=[]#(lat,lon,response_min,unit_type,date)
with open('../data/incidents_with_latlongs.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=';')
        next(reader)#skip first row with headers
        for row in reader:
                try:
                        incidents.append((float(row[15]),float(row[16]),float(row[7]),str(row[1]),str(row[5])))
                except ValueError:
                        continue
myServer = HTTPServer((hostName,hostPort), MyServer)

print("Server Started")

try:
        myServer.serve_forever()
except KeyboardInterrupt:
        pass

myServer.server_close()
print("Server Stopped")
