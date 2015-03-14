#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
hostPort = 80

def handle_latlon(path):
	(lat_s,lon_s)=path[1:].split(",",1)
	(lat,lon)=(float(lat_s),float(lon_s))
	print(lat)
	print(lon)

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		handle_latlon(self.path)
		self.wfile.write(bytes("<html><body><p>seb</p></body></html>","utf-8"))

myServer = HTTPServer((hostName,hostPort), MyServer)
print("Server Started")

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print("Server Stopped")
