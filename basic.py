from pymodule.easymodbus.modbusClient import *
import ast
import struct
import codecs



modbusClient = ModbusClient("/dev/ttyS0")
#modbusClient = ModbusClient("/dev/tty.usbserial-14310")
modbusClient.parity = Parity.none
modbusClient.baudrate = 9600
modbusClient.stopbits = Stopbits.one
modbusClient.unitidentifier = 1
modbusClient.connect()



# StartAddressA = 16384
# dataA = modbusClient.read_holdingregisters(StartAddressA,125)

StartAddress_A = 19000
data_A = modbusClient.read_holdingregisters(StartAddress_A, 120)



print(dataA)
#print(dataB)


