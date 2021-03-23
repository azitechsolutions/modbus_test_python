from pymodule.easymodbus.modbusClient import *

modbusClient = ModbusClient("/dev/ttyS0")
modbusClient.parity = Parity.none
modbusClient.baudrate = 9600
modbusClient.stopbits = Stopbits.one
modbusClient.unitidentifier = 10
modbusClient.connect()

data = modbusClient.read_holdingregisters(796,2)
print(data)
