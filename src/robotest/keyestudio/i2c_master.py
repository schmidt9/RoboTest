# https://dronebotworkshop.com/i2c-arduino-raspberry-pi/

from smbus3 import SMBus

addr = 0x8 # bus address
start_register = 0x00
bus = SMBus(2) # indicates /dev/i2c-2


def send_byte_command(command: int):
    bus.write_byte(addr, command)
    byte_value = bus.read_byte(addr)
    str_byte_value = byte_value.to_bytes(1, 'big').decode('utf-8')
    print(f'Byte read: {byte_value} (string value: {str_byte_value})')


def send_str_command(command: str):
    try:
        command_bytes = command.encode("utf-8");
        bus.write_block_data(addr, start_register, command_bytes)

        bytes_value = bus.read_block_data(addr, start_register)
        str_bytes_value = bytes_value.decode('utf-8')
        print(f'Bytes read string value: {str_bytes_value})')
    except IOError as e:
        print(f"Error writing/reading data: {e}")
    finally:
        # It's good practice to close the bus when done
        bus.close()


if __name__ == '__main__':
    print ("Enter command")

    while True:
        command = input('>>>>   ').encode('utf-8')
        send_byte_command(command[0])



