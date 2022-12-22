#!/usr/bin/python3

# For testing in different situations
USING_GPIO=True
USE_LOG=True
USE_BME280=False

# File paths
datadir="/home/pi/Desktop/STC-clock/Data/"
logfile=datadir+"interrupts.log"
setfile=datadir+"setting.txt"

#
# Set up to read bme280 sensor
#
import smbus2

if USE_BME280:
  import bme280
  # Change bus and ID for the particular sensor config
  bme280_bus = smbus2.SMBus(1)
  bme280_ID = 0x76
  bme280_calibration = bme280.load_calibration_params(bme280_bus)

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

    interrupt_pin = 22
    # GPIO set up as input. It is pulled up to stop false signals
    GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
#
# Main loop waiting for interrupt
#
while True:
    try:
        if USING_GPIO: GPIO.wait_for_edge(interrupt_pin, GPIO.FALLING)
        interrupt_time = datetime.datetime.now()
        
        # Get the current Fine Adjust setting and add the time of the interrupt
        with open(setfile) as f:
            info = f.readline().rstrip() + \
              " " + str(interrupt_time)

        # Read the current sensor data if applicable
        if USE_BME280:
          bme280_data = bme280.sample(bme280_bus,bme280_ID,bme280_calibration)

          # Construct the information line for the log
          info = info + \
            " " + "{:.2f}".format(bme280_data.temperature) + \
            " " + "{:.2f}".format(bme280_data.pressure) + \
            " " + "{:.2f}".format(bme280_data.humidity)

        # Log the data
        if USE_LOG:
            logger.info(info)
            time.sleep(30) # anything within 30s may be chiming the same hour. Don't wait too long as there are occasional false triggers
        else:
            print(info)
            
    except:
        if USE_LOG:
            logger.error("Exception detected, continuing:", sys.exc_info()[0])
        else:
            raise
    
GPIO.cleanup()           # clean up GPIO on normal exit  
