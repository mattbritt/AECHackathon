#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X
import RPi.GPIO as GPIO

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
tof = VL53L0X.VL53L0X(address=0x2B)
tof1 = VL53L0X.VL53L0X(address=0x2D)

# Set shutdown pin high for the first VL53L0X then 
# call to start ranging 
GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof.start_ranging(VL53L0X.VL53L0X_HIGH_SPEED_MODE)
#tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Set shutdown pin high for the second VL53L0X then 
# call to start ranging 
GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof1.start_ranging(VL53L0X.VL53L0X_HIGH_SPEED_MODE)
#tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

MAX_DIST = 500		# Maximum distance for Valid Measurement

VALID_TIME_LIMIT = .5	# Time to keep a minimum value

HEIGHT_FOR_MIN = 100 	# Number of mm for a min to be a min

minDist1 = MAX_DIST + 1
minTime1 = 0
isValid1 = False

minDist2 = MAX_DIST + 1
minTime2 = 0
isValid2 = False

while True:
	distance1 = tof.get_distance()
	time1 = time.time()
	distance2 = tof1.get_distance()
	time2 = time.time()

	# Check for a new minimum reading
	if (distance1 > 0 and distance1 < MAX_DIST and distance1 < minDist1):
		minDist1 = distance1
		minTime1 = time1
		isValid1 = False
#		print ("New Min Reading")

	# Check if found minimum
	if (distance1 > (minDist1 + HEIGHT_FOR_MIN) and (time1 - minTime1) < VALID_TIME_LIMIT):
		isValid1 = True
#		print ("Found Minimum 1")

	# Make Min invalid if too old
	if ((time1 - minTime1) > VALID_TIME_LIMIT):
		minDist1 = MAX_DIST + 1
		minTime1 = 0
		isValid1 = False
#		print ("Min is stale")

#	if isValid1:
#		minDist1 = MAX_DIST + 1
#		minTime1 = 0
#		isValid1 = False
#		print ("New Min 1\n")

	# Check for a new minimum reading
	if (distance2 > 0 and distance2 < MAX_DIST and distance2 < minDist2):
		minDist2 = distance2
		minTime2 = time2
		isValid2 = False
#		print ("New Min Reading")

	# Check if found minimum
	if (distance2 > (minDist2 + HEIGHT_FOR_MIN) and (time2 - minTime2) < VALID_TIME_LIMIT):
		isValid2 = True
#		print ("Found Minimum 2")

	# Make Min invalid if too old
	if ((time2 - minTime2) > VALID_TIME_LIMIT):
		minDist2 = MAX_DIST + 1
		minTime2 = 0
		isValid2 = False
#		print ("Min is stale")

#	if isValid2:
#		minDist2 = MAX_DIST + 1
#		minTime2 = 0
#		isValid2 = False
#		print ("New Min 2\n)

#	print ("Min1 = %5d, Time1 = %18f, Valid1 = %d, Min2 = %5d, Time2 = %18f, Valid2 = %d" % (minDist1, minTime1, isValid1, minDist2, minTime2, isValid2))

	if (isValid1 and isValid2):
		if (minTime1 < minTime2):
			print ("\nForward\n")
		else:
			print ("\nBackward\n")
		minDist1 = MAX_DIST + 1
		minTime1 = 0
		isValid1 = False
		minDist2 = MAX_DIST + 1
		minTime2 = 0
		isValid2 = False

#	if (distance1 > 0 and distance2 > 0):
#		print ("Sensor 1 - %4d mm, Sensor 2, %4d mm" % (distance1, distance2))
#	else:
#		print ("%d - Error" % tof.my_object_number)

#	print ("Sleep for %f seconds" % (timing/1000000.00))

	time.sleep(timing/1000000.00)

tof1.stop_ranging()
GPIO.output(sensor2_shutdown, GPIO.LOW)
tof.stop_ranging()
GPIO.output(sensor1_shutdown, GPIO.LOW)

