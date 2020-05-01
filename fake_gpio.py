_PRINT_OUTPUT=False
BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = True
LOW = False

def output(pins, value):
    if _PRINT_OUTPUT: print("GPIO.output:", pins, value)

def setmode(value):
    print("GPIO.setmode:", value)

def setup(pins, value, initial=LOW):
    print("GPIO.setup:", value)
    output(pins, initial)

def cleanup():
    print("GPIO.cleanup")
    
