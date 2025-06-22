import serial
import time
import serial.tools.list_ports

if __name__ == '__main__':
    
    port = ""
    ports = list(serial.tools.list_ports.comports())
    
    for p in ports:
        if p.device.startswith("/dev/ttyUSB"):
            port = p.device
            break

    try:
        ser = serial.Serial(port, 115200, timeout=1)
        ser.flush()

        print(f"Connected to {port}")

        read_command = "r"
        command = ""
    
        while True:
            if command != read_command:
                command = input("Enter command: ")

                if command != read_command:
                    ser.write(command.encode('utf-8') + b'\n')
                else: 
                    print("Read mode on")

            lines = ser.readlines()

            for line in lines:
                line = line.decode("utf-8").rstrip()

                if len(line) > 0:
                    print(f"Response: {line}")

            time.sleep(0.5)

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            print("closing serial")
            ser.close()
            
