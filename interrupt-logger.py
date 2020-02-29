#!/usr/bin/python3

# For testing in diffierent situations
USING_GPIO=False
datadir="/home/pi/Desktop/STC-clock/Data/"
logfile=datadir+"interrupts.log"
setfile=datadir+"setting.txt"

# Set up rotating log file
import logging
import time
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
# Set up log to rotate daily
handler = TimedRotatingFileHandler(logfile,
                                   when="d",
                                   interval=1,
                                   backupCount=0)
logger.addHandler(handler)

# Set up interrupt handler
if USING_GPIO:
    import RPi.GPIO as GPIO  
    GPIO.setmode(GPIO.BCM)  

    interrupt_pin = 2
    # GPIO set up as input. It is pulled up to stop false signals
    GPIO.setup(interrupt_pin, GPIO.IN) # pin 2 has pull up already, pull_up_down=GPIO.PUD_UP)  

import datetime
    
while True:
    if USING_GPIO: GPIO.wait_for_edge(interrupt_pin, GPIO.FALLING)
    interrupt_time = datetime.datetime.now()
    with open(setfile) as f:
        current_setting = f.readline().rstrip()
    logger.info(current_setting + " " + str(interrupt_time))
    time.sleep(1) # anything less than 1 second is a bounce
    
GPIO.cleanp()           # clean up GPIO on normal exit  
