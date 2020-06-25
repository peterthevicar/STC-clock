import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  

D1 = 22
D2 = 27
GPIO.setup(D1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Interesting callback handler method of waiting for interrupts
# ~ def my_callback(channel):
    # ~ print('Edge detected on channel {}'.format(channel))
    # ~ print('Strike:',GPIO.input(D1),'Release:',GPIO.input(D2), end='\r')
# ~ GPIO.add_event_detect(D1, GPIO.FALLING, callback=my_callback)
# ~ GPIO.add_event_detect(D2, GPIO.FALLING, callback=my_callback)

# Loop to show current state of pins
while True:
    print('Strike:',GPIO.input(D1),'Release:',GPIO.input(D2), end='\r')
    time.sleep(0.1)
