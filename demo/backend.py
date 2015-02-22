#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
hostPort = 80

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><body><p>seb</p></body></html>","utf-8"))

myServer = HTTPServer((hostName,hostPort), MyServer)
print("Server Started")

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print("Server Stopped")
