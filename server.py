#!/usr/bin/env python3
from bottle import post, route, run, static_file, request
import serial
import sys
import time

# Connect to serial port
port_file = open("comport.txt", "r")
ser = None
for line in port_file.readlines():
  port = line.strip()
  try:
    if not ser:
      print("Trying", port)
      ser = serial.Serial(port, timeout=1)
  except serial.serialutil.SerialException as e:
    print("Serial port failure: " + str(e))
port_file.close()
if not ser:
  sys.exit(1)
time.sleep(1)
line = ser.readline()
print(line.strip())
while line != b"":
  time.sleep(1)
  line = ser.readline()
  print(line.strip())

@route('/')
def index():
  return static_file('index.html', root="static")
  
@route('/<filename:path>')
def serve_static(filename):
  return static_file(filename, root="static")

@post('/set_values')
def set():
  req = request.json
      
  # Write it
  cmd = ""
  for (chan, val) in req["lights"]:
    cmd += "%sc%sw" % (chan, val)
  print(cmd)
  ser.write(str.encode(cmd))
  #ser.read()

  # Send back OK
  return {'ok': True}

print("Browse to http://localhost:8000")
run(host='localhost', port=8000)

