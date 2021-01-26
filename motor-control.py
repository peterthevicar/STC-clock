#!/usr/bin/python
"""
Send the right signals to the stepper motor to move the fine adjustment weight
Always finish by moving the weight UP a little to overcome hysteresis
Keep settings.txt up to date with the current position of the weight
Check the weight doesn't move too far in either direction
"""
# File where the current position of the weight is recorded
datadir="/home/pi/Desktop/STC-clock/Data/"
setfile=datadir+"setting.txt"

# Import required libraries
import sys
import time
try:
    import RPi.GPIO as GPIO
except:
    import fake_gpio as GPIO
 
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
 
# Define GPIO pins to use to drive the motor
# In order    Bu, Pi, Y, Or (same as motor driver board)
motor_pins = (4, 14, 15, 18)
 
# Set all pins as output, set HIGH as the motor driver inverts the sense
GPIO.setup(motor_pins, GPIO.OUT, initial=GPIO.HIGH)

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
STEPS_PER_SEQ = len(motor_seq)
def one_seq(direction):
    """
    Go through one whole sequence, in either direction.
    Don't stop mid-sequence as it makes re-starts unreliable
    """
    global STEPS_PER_SEQ
    
    # Always FINISH on step 0
    step = 1 if direction == 1 else STEPS_PER_SEQ-1
    for i in range(STEPS_PER_SEQ):
        GPIO.output(motor_pins, motor_seq[step % STEPS_PER_SEQ])
        step += direction
         
        # Wait between steps. 0.005 is the fastest it can go reliably
        time.sleep(0.01)

# 360° rotation requires 128 times through the sequence (1024 individual steps)
# Adjust SEQS_PER_TENTH according to size of scale: 
#   number of sequences of the motor needed to shift the weight by 
#   one tenth of a major tick on the pendulum scale
#   32 seems just right for current scale
# Need to stick with a whole number
SEQS_PER_TENTH = 32

try:
    # Read what we're trying to achieve from the input, format is <+|-><number of tenths>
    inline = sys.stdin.readline()

    # First the direction: positive increment turns the motor shaft clockwise.
    # Motor is at the top of the screw so screw goes anti-clockwise and the 
    # weight goes down the bob towards 10
    if inline[0] == "+":
        direction = 1
    elif inline[0] == "-":
        direction = -1
    else:
        raise "Invalid input, should be <+|-><ntenths>"

    # Rest of input line is the number of tenths to move; translate into seqs
    ntenths = int(inline[1:])

    # Boundary check, mustn't go outside 1.0 - 10.9
    with open(setfile, "r") as f:
        current_setting = float(f.read())
        if direction == -1:
            ntenths = min(ntenths, int((current_setting - 1.0) * 10))
        else:
            ntenths = min(ntenths, int((10.9 - current_setting) * 10))
    
    # Do the move, keeping the settings file updated every tenth of a tick
    print("Moving "+str(ntenths)+" tenths from "+str(current_setting))
    for t in range (ntenths):
        for i in range(SEQS_PER_TENTH):
            one_seq(direction)
        current_setting += direction * 0.1
        with open(setfile, "r+") as f:
            f.write("{:.1f}".format(current_setting))
            f.truncate()
        print("{:.1f}".format(current_setting))

finally:
    # Important to switch off the magnets to avoid over-heating
    GPIO.cleanup()
