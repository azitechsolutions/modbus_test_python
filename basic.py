from pymodule.easymodbus.modbusClient import *
import ast
import struct
import codecs



modbusClient = ModbusClient("/dev/ttyS0")
modbusClient.parity = Parity.none
modbusClient.baudrate = 9600
modbusClient.stopbits = Stopbits.one
modbusClient.unitidentifier = 1
modbusClient.connect()



StartAddressA = 3900
dataA = modbusClient.read_holdingregisters(StartAddressA,100)

print(dataA)
#print(dataB)

