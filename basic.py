from pymodule.easymodbus.modbusClient import *
import ast
import struct
import codecs



modbusClient = ModbusClient("/dev/ttyS0")
modbusClient.parity = Parity.none
modbusClient.baudrate = 9600
modbusClient.stopbits = Stopbits.one
modbusClient.unitidentifier = 3
modbusClient.connect()



StartAddressA = 11776
dataA = modbusClient.read_holdingregisters(StartAddressA,32)

print(dataA)
#print(dataB)


