#!/usr/bin/env python2.7  
# script by Alex Eames https://raspi.tv/  
# https://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio  
import datetime
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  

interrupt_pin = 2
# GPIO set up as input. It is pulled up to stop false signals  
GPIO.setup(interrupt_pin, GPIO.IN) # pin 2 has pull up already, pull_up_down=GPIO.PUD_UP)  
  
print ("Waiting for falling edge on GPIO", interrupt_pin)  
# now the program will do nothing until the signal on port 23   
# starts to fall towards zero. This is why we used the pullup  
# to keep the signal high and prevent a false interrupt  
  
while True:
    GPIO.wait_for_edge(interrupt_pin, GPIO.FALLING)  
    print (datetime.datetime.now())
GPIO.cleanup()           # clean up GPIO on normal exit  