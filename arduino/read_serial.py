#!/usr/bin/python

import serial
import time

ser = serial.Serial("COM7", 9600, timeout=1)
time.sleep(1)
line = ser.readline()
print line
while line != "":
	time.sleep(1)
	line = ser.readline()
	print line
