#!/usr/bin/env python3
from bottle import post, route, run, static_file, request, SimpleTemplate
import sys
import time
import configparser

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
    for (chan, val) in values:
      cmd += "%sc%sw" % (chan, val)
    self.ser.write(str.encode(cmd))

class NullController():
  def __call__(self, values):
    for (chan, val) in values:
      print( str(chan) + ' => ' + str(val) )

class uDMXController():
  def __init__(self):
    import usb
    dev = usb.core.find(idVendor=0x16c0, idProduct = 0x05dc)
    if dev != None and (dev.manufacturer != 'www.anyma.ch' or dev.product != 'uDMX'):
      dev = None
    if not dev:
      print("Could not find device")
      sys.exit(1)
    self.dev = dev
    self.reqType = usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE | usb.util.ENDPOINT_OUT

  def write_one(self, channel, value):
    # request 1 means set single channel, wValue = value, wIndex = channel, wLength is ignored
    return self.dev.ctrl_transfer(self.reqType, 1, value, channel) == 0

  def write_many(self, start_channel, values):
    # request 2 means set multiple channels, wValue = number of values, wIndex = starting channel
    return self.dev.ctrl_transfer(self.reqType, 2, len(values), start_channel, values) == len(values)

  def __call__(self, values):
    for (chan, val) in values:
      self.write_one(chan, val)


if __name__ == "__main__":
  # Setup
  c = configparser.ConfigParser()
  c.read('config.ini')

  ctrl = NullController()
  if c['settings']['controller'] == 'uDMX':
    ctrl = uDMXController()
  elif c['settings']['controller'] == 'Arduino':
    ctrl = ArduinoController()

  if 'static' in c:
    ctrl(c['static'].items())

  template_info = []
  for sec in filter(lambda x: x.startswith('fixture-'), c.keys()):
    template_info.append({'title': c[sec]['name'], 'id': sec})

  indexTemplate = SimpleTemplate(open('index.tpl.html', 'r')).render(fixtures=template_info)

  # Webserver
  @route('/')
  def index():
    return indexTemplate
    
  @route('/<filename:path>')
  def serve_static(filename):
    return static_file(filename, root="static")

  @post('/set_values')
  def set():
    vals = []
    base = int(c[request.json['id']]['base'])
    for col in ['r','g','b']:
      vals.append( (base, request.json[col]) )
      base += 1
    ctrl(vals)
    return {'ok': True}

  print("Browse to http://localhost:8000")
  run(host='localhost', port=8000)

