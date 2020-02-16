#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO
 
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
 
# Define GPIO signals to use
# In order [Y,Pi,Bu,O]
StepPins = [15,14,4,18]
 
# Set all pins as output
# According to raspberry-gpio-python documentation (https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/) 
# you can output to several channels at the same time by passing 2 list parameters instead of 2 integers.
for pin in StepPins:
  print("Setup pins")
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False) # the ULN2003 driver inverts the voltage, i.e. True is 0v

# Define advanced sequence
# as shown in manufacturer's datasheet (these are reversed, i.e. 1 = 0v) see above
# Sequence starts at step 2 (step 1 is Orange only at 0v)
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
 
StepCount = len(Seq)
StepDir = 1 # Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise
 
# Read wait time from command line
if len(sys.argv) > 1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 10/float(1000)
 
# Initialise variables
StepCounter = 0
 
# Start main loop
while True:
 
  print(StepCounter, Seq[StepCounter])
 
  for pin in range(0, 4):
    xpin = StepPins[pin]#
    if Seq[StepCounter][pin]!=0:
      print(" Enable GPIO", pin)
      GPIO.output(xpin, True)
    else:
      GPIO.output(xpin, False)
 
  StepCounter += StepDir
 
  # If we reach the end of the sequence
  # start again
  if (StepCounter >= StepCount):
    StepCounter = 0
  if (StepCounter < 0):
    StepCounter = StepCount+StepDir
 
  # Wait before moving on
  time.sleep(WaitTime)