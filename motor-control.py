#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO
 
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
 
# Define GPIO pins to use to drive the motor
# In order    Bu, Pi, Y, O (same as motor driver board)
motor_pins = (4, 14, 15, 18)
 
# Set all pins as output
# According to raspberry-gpio-python documentation at
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/
# you can output to several channels at the same time
# by passing 2 list parameters instead of 2 integers.
GPIO.setup(motor_pins, GPIO.OUT)

# Sequence of outputs to the motor_pins to turn the motor clockwise,
# as shown in manufacturer's datasheet.
# These are reversed, i.e. 1 = 0v, because the ULN2003 inverts the voltage
motor_seq = (
    (0,0,0,1),
    (0,0,1,1),
    (0,0,1,0),
    (0,1,1,0),
    (0,1,0,0),
    (1,1,0,0),
    (1,0,0,0),
    (1,0,0,1)
    )
 
step_count = len(motor_seq)
# Set step_inc to +/-1 or +/-2. 1 gives half speed, high torque.
# Positive increment turns the shaft clockwise, negative anti-clockwise
# The duration of a 360° rotation is wait_sec*(step_count/step_inc)*128
# so for an increment of 1 you get wait_sec*1024 per rotation
step_inc = int(input("increment (-2,-1,1,2): "))
 
# Read wait time from terminal
wait_sec = float(input("Wait time (s): "))
 
# Initialise variables
step_n = 0
 
# Start main loop
try:
    while True:
      GPIO.output(motor_pins, motor_seq[step_n]) 
      step_n += step_inc
     
      # loop at end of sequence
      if (step_n >= step_count):
        step_n = 0
      elif (step_n < 0):
        step_n = step_count + step_inc
     
      # Wait between steps
      time.sleep(wait_sec)

finally:
    GPIO.output(motor_pins, False)