BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = True
LOW = False

def output(pins, value):
  print("GPIO.output:", pins, value)

def setmode(value):
    print("GPIO.setmode:", value)

def setup(pins, value, initial=LOW):
    print("GPIO.setup:", value)
    output(pins, initial)

def cleanup():
    print("GPIO.cleanup")
    
