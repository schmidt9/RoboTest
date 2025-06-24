# https://dronebotworkshop.com/i2c-arduino-raspberry-pi/

from smbus3 import SMBus

addr = 0x8 # bus address
bus = SMBus(2) # indicates /dev/i2c-2

numb = 1

print ("Enter command")


def send_command(command: int):
    bus.write_byte(addr, command)
    byte_value = bus.read_byte(addr)
    str_byte_value = byte_value.to_bytes(1, 'big').decode('utf-8')
    print(f'Byte read: {byte_value} (string value: {str_byte_value})')


while numb == 1:
    command = input('>>>>   ').encode('utf-8')
    send_command(command[0])



