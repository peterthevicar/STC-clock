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
 
STEP_COUNT = len(motor_seq)
# Set step_inc to +/-1 or +/-2. 1 gives half speed, high torque.
# Positive increment turns the shaft clockwise, negative anti-clockwise
# The duration of a 360° rotation is wait_sec*(step_count/step_inc)*128
# so for an increment of 1 you get wait_sec*1024 per rotation
STEP_INC = 1
STEPS_PER_REV = STEP_COUNT/STEP_INC*128
REVS_PER_UNIT = 2.5 # Number of turns of the motor to shif the weight by one unit on the pendulum scale
WAIT_SEC = 0.01 # 0.005 is the fastest it can go reliably

# Read what we're trying to achieve from the input
inline = sys.sdin.readline()
if inline[0] == "+":
    direction = 1
elif inline[0] == "-":
    direction = -1
else
    raise "Invlaid input, should be +n or -n)"
step_inc = STEP_INC * direction

# Rest of input line is the number of units to move; translate into steps
total_steps = int(inline[1:]) * STEPS_PER_REV * REVS_PER_UNIT

# Initialise variables
step_n = 0
 
# Start moving
try:
    while steps_left > 0:
      GPIO.output(motor_pins, motor_seq[step_n])
      step_n += step_inc
      steps_left -= 1
     
      # loop at end of sequence
      if (step_n >= step_count):
        step_n = 0
      elif (step_n < 0):
        step_n = step_count + step_inc
     
      # Wait between steps
      time.sleep(WAIT_SEC)

finally:
    GPIO.output(motor_pins, False)