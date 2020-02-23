#!/usr/bin/python3

# Set up rotating log file
import logging
import time
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
# Set up log to rotate daily
handler = TimedRotatingFileHandler("/home/pi/Desktop/STC-clock/interrupts.log",
                                   when="d",
                                   interval=1,
                                   backupCount=0)
logger.addHandler(handler)

# Set up interrupt handler
import datetime
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  

interrupt_pin = 2
# GPIO set up as input. It is pulled up to stop false signals
GPIO.setup(interrupt_pin, GPIO.IN) # pin 2 has pull up already, pull_up_down=GPIO.PUD_UP)  
    
while True:
    GPIO.wait_for_edge(interrupt_pin, GPIO.FALLING)
    logger.info(datetime.datetime.now())
    time.sleep(1) # anything less than 1 second is a bounce
    
GPIO.cleanp()           # clean up GPIO on normal exit  
