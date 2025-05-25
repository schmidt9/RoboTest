# https://dronebotworkshop.com/i2c-arduino-raspberry-pi/

from smbus3 import SMBus
 
addr = 0x3c # bus address
bus = SMBus(2) # indicates /dev/i2c-2

bus.write_byte(addr, 0x1)
