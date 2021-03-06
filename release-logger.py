#!/usr/bin/python3

# For testing in different situations
USING_GPIO=True
USE_LOG=True

# File paths
datadir="/home/pi/Desktop/STC-clock/Data/"
logfile=datadir+"release.log"
setfile=datadir+"setting.txt"

#
# Set up rotating log file
#
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import time

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
# Set up log to rotate daily
# End the day at 23.45 so midnight starts the next log
handler = TimedRotatingFileHandler(logfile,
                                   when="midnight",
                                   atTime=datetime.time(23,45),
                                   interval=1,
                                   backupCount=400)
logger.addHandler(handler)
#
# Set up interrupt handler
#
if USING_GPIO:
    import RPi.GPIO as GPIO  
    GPIO.setmode(GPIO.BCM)  

    interrupt_pin = 27
    # GPIO set up as input. It is pulled up to stop false signals
    GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
#
# Main loop waiting for interrupt
#
while True:
    try:
        # The release sensor is normally 0, goes slowly to 1 about 
        # 5 mins before release then back to 0 quickly on release
        # Likely to get at least one falling edge on the slow way up
        if USING_GPIO: GPIO.wait_for_edge(interrupt_pin, GPIO.FALLING)
        interrupt_time = datetime.datetime.now()
        
        # Construct the information line for the log
        info = interrupt_time
          
        # Log the data
        if USE_LOG:
            logger.info(info)
            time.sleep(60) # anything within 1 minute is just bounce on the way up
        else:
            print(info)
            time.sleep(1)
            
    except:
        if USE_LOG:
            logger.error("Exception detected, continuing:", sys.exc_info()[0])
        else:
            raise
    
GPIO.cleanup()           # clean up GPIO on normal exit  
