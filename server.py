#!/usr/bin/python
import BaseHTTPServer, SimpleHTTPServer
import json
import serial

# Connect to serial port
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
line = ser.readline()
print line.strip()
while line != "":
  line = ser.readline()
  print line.strip()

# Request handling
class ReqHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  # Handle ordinary GET / HEAD requests in the static subfolder
  def do_GET(self):
    self.path = '/static' + self.path
    SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
  def do_HEAD(self):
    self.path = '/static' + self.path
    SimpleHTTPServer.SimpleHTTPRequestHandler.do_HEAD(self)

  # Handle posts only if they are json requests
  def do_POST(self):
    if self.headers['Content-Type'] == 'application/json' and self.path == "/set_values":
      # Grab data from request
      self.data_string = self.rfile.read(int(self.headers['Content-Length']))
      req = json.loads(self.data_string)
      
      # Write it
      for (chan, val) in req["lights"]:
        cmd = "%sc%sw" % (chan, val)
        ser.write(cmd)
        ser.read()
      print req

      # Send back OK
      resp = json.dumps( {'ok': True} )
      self.send_response(200)
      self.send_header("Content-Length", len(resp))
      self.send_header("Content-Type", "application/json")
      self.end_headers()
      self.wfile.write(resp)
    else:
      self.send_response(400)

httpd = BaseHTTPServer.HTTPServer(('', 8000), ReqHandler)
httpd.serve_forever()
