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

# Now the sensor interrupt pin
interrupt_pin = 2
# GPIO set up as input. It is pulled up to stop false signals  
GPIO.setup(interrupt_pin, GPIO.IN) # pin 2 has pull up already, pull_up_down=GPIO.PUD_UP)  

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

# Set step_inc to 1 or 2. 1 gives half speed, high torque.
# A 360° rotation takes 16*64=1024 single steps (16*8=512 double steps)
# so for an increment of 1 you get wait_sec*1024 per rotation
step_inc = 1
 
# Wait time between steps. Fastest possible is 0.002 seconds
wait_sec = 0.01
 
# Assume motor is currently at step 0 (may be wrong but can't tell)
step_n = 0

def turn_steps(n_steps, cw=True):
    """
    Turn the motor by n_steps clockwise. cw=False means anti-clockwise
    """
    global step_n
    
    inc = step_inc if cw else -step_inc
    for i in range(n_steps):
        step_n += inc

        # loop at end of sequence
        if (step_n >= step_count): step_n = 0
        elif (step_n < 0): step_n = step_count + inc

        # Turn the motor
        GPIO.output(motor_pins, motor_seq[step_n]) 

        # Wait between steps
        time.sleep(wait_sec)
    # Power off the stepper motor
    GPIO.output(motor_pins, 0)
    
# Start main loop
try:
    while True:
        GPIO.wait_for_edge(interrupt_pin, GPIO.FALLING)  
        turn_steps(128, True)
finally:
    GPIO.output(motor_pins, False)
    GPIO.cleanup()