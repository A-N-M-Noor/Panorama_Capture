import serial
from serial.tools import list_ports

ports = list_ports.comports()
for port in ports:
    print(port.device)
    print(port.description)
    print(port.hwid)
    print(port.manufacturer)
    print(port.product)
    print(port.serial_number)
    print(port.vid)
    print(port.pid)
    print(port.location)
    print(port.interface)
    print("----------")

# ser = serial.Serial("/dev/ttyACM0", 115200)
# while(not ser.is_open):
#     pass
# print("Serial port open")
# ser.close()