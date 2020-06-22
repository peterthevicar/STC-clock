import smbus2
import bme280

data = bme280.sample(smbus2.SMBus(1),0x76,bme280.load_calibration_params(smbus2.SMBus(1)))
print (data)
