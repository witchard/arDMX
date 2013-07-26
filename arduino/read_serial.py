#!/usr/bin/python

import serial
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
line = ser.readline()
print line
while line != "":
	line = ser.readline()
	print line
