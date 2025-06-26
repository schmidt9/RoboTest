# https://dronebotworkshop.com/i2c-arduino-raspberry-pi/

from smbus3 import SMBus

addr = 0x8  # bus address
start_register = 0x00
bus = SMBus(2)  # indicates /dev/i2c-2
max_block_size = 32  # I2C_SMBUS_BLOCK_MAX


def send_byte_command(command: int):
    bus.write_byte(addr, command)
    byte_value = bus.read_byte(addr)
    str_byte_value = byte_value.to_bytes(1, "big").decode("utf-8")
    print(f"Byte read: {byte_value} (string value: {str_byte_value})")


def send_str_command(command: str):
    try:
        command_bytes = command.encode("utf-8")
        print(f"Sending string '{command}' (bytes: {command_bytes})")
        bus.write_i2c_block_data(addr, start_register, command_bytes)

        bytes_value = bus.read_i2c_block_data(addr, start_register, max_block_size)
        bytes_value_str = ""

        for byte in bytes_value:
            if byte == 255:
                break
            else:
                bytes_value_str += chr(byte)

        print(f"Bytes read string value: {bytes_value_str})")
    except IOError as e:
        print(f"Error writing/reading data: {e}")


if __name__ == "__main__":
    print("Enter command")

    while True:
        command = input(">>>>   ").encode("utf-8")
        send_byte_command(command[0])
