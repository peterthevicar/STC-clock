#!/usr/bin/python3

# For testing in diffierent situations
USING_GPIO=True
datadir="/home/pi/Desktop/STC-clock/Data/"
logfile=datadir+"interrupts.log"
setfile=datadir+"setting.txt"

# Each temperature sensor has a different address so if you change the sensor change this
temp_sensor="/sys/bus/w1/devices/28-00181100004b/w1_slave"

# Set up rotating log file
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

# Set up interrupt handler
if USING_GPIO:
    import RPi.GPIO as GPIO  
    GPIO.setmode(GPIO.BCM)  

    interrupt_pin = 2
    # GPIO set up as input. It is pulled up to stop false signals
    GPIO.setup(interrupt_pin, GPIO.IN) # pin 2 has pull up already, pull_up_down=GPIO.PUD_UP)  

while True:
    if USING_GPIO: GPIO.wait_for_edge(interrupt_pin, GPIO.FALLING)
    interrupt_time = datetime.datetime.now()
    with open(setfile) as f:
        current_setting = f.readline().rstrip()
    try:
        with open(temp_sensor) as f:
            t=(f.read().split("t="))[1].rstrip()
            t=(float(t)/1000)
    except FileNotFoundError:
        t=-99
    logger.info(current_setting + " " + str(interrupt_time) + " " + str(t))
    time.sleep(60) # anything within 1 minute is chiming the same hour. Don't wait too long as there are occasional false triggers
    
GPIO.cleanup()           # clean up GPIO on normal exit  
