#!/usr/bin/env python3
from bottle import post, route, run, static_file, request
import sys
import time

class ArduinoController():
  def __init__(self):
    import serial
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
    self.ser = ser

  def __call__(self, values):
    cmd = ""
    for (chan, val) in req["lights"]:
      cmd += "%sc%sw" % (chan, val)
    self.ser.write(str.encode(cmd))

class NullController():
  def __call__(self, values):
    for (chan, val) in values:
      print( str(chan) + ' => ' + str(val) )

ctrl = ArduinoController()

@route('/')
def index():
  return static_file('index.html', root="static")
  
@route('/<filename:path>')
def serve_static(filename):
  return static_file(filename, root="static")

@post('/set_values')
def set():
  req = request.json
      
  ctrl(req['lights'])

  # Send back OK
  return {'ok': True}

print("Browse to http://localhost:8000")
run(host='localhost', port=8000)

