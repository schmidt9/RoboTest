import serial
import time

# Открываем Serial порт ('COMX' замените на имя вашего порта)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = .1)
# Отправляем строку "Hello, Arduino!" на Arduino, предварительно преобразовав ее в байты
ser.write(b'Hello, Arduino!')
# Читаем ответ от Arduino через Serial порт
time.sleep(0.05)
response = ser.readline()
# Декодируем ответ из байтов в строку с использованием UTF-8
decoded_response = response.decode('utf-8')
# Закрываем порт
ser.close()
print(decoded_response)
