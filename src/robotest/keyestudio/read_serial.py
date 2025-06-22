import serial

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)

while True:
    data = arduino.readline()

    if len(data) > 0:
        print(data)
