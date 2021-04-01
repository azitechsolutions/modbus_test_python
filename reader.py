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

def int32bits(hexstr):
    dec = int(hexstr,16)
    value = dec
    if value & (1 << (32-1)):
        value -= 1 << 32
    return value
def int16bits(hexstr):
    value = int(hexstr,16)
    if value & (1 << (16-1)):
        value -= 1 << 16
    return value

def UINT32toFloat(register, startRegister, dataArray):
    hex1 = "%02x" % int(dataArray[(register - startRegister)-1])
    hex2 = "%02x" % int(dataArray[register - startRegister])

    for i in range(len(hex1),4):
        hex1 = "0{}".format(hex1)
    for i in range(len(hex2),4):
        hex2 = "0{}".format(hex2)

    joinHex = "{}{}".format(hex1,hex2)

    flotingPoint = struct.unpack('!f', codecs.decode(joinHex, 'hex'))[0]
    
    result = ("%.2f" % flotingPoint)
    
    return round(float(result), 2)
def UINT32toFloat_V2(register, startRegister, dataArray):
    hex1 = "%02x" % int(dataArray[(register - startRegister)])
    hex2 = "%02x" % int(dataArray[(register - startRegister)+1])

    for i in range(len(hex1),4):
        hex1 = "0{}".format(hex1)
    for i in range(len(hex2),4):
        hex2 = "0{}".format(hex2)

    joinHex = "{}{}".format(hex1,hex2)

    flotingPoint = struct.unpack('!f', codecs.decode(joinHex, 'hex'))[0]
    
    result = ("%.2f" % flotingPoint)
    
    return round(float(result), 2)
def UINT32(register, startRegister, dataArray):
    low = dataArray[register-startRegister]
    high = dataArray[(register-startRegister)-1] 

    # print("Data Array: {}    Low:{}   High: {}".format(dataArray,low,high))
    val = (high * 65536) + low 
    result = ("%.2f" % val)
    return round(float(result), 2)
def UINT32_V2(register, startRegister, dataArray):
    high = dataArray[register-startRegister]
    low = dataArray[(register-startRegister)+1] 

    # print("Data Array: {}    Low:{}   High: {}".format(dataArray,low,high))
    val = (high * 65536) + low 
    result = ("%.2f" % val)
    return round(float(result), 2)
def UINT32_V3(register, startRegister, dataArray):
    high = dataArray[register-startRegister]
    mid = dataArray[(register-startRegister)+1] 
    low = dataArray[(register-startRegister)+2] 

    # print("Data Array: {}    Low:{}   High: {}".format(dataArray,low,high))
    val = ((high * 65536 * 65536) + (mid*65536)+ low )
    result = ("%.2f" % val)
    return round(float(result), 2)
def INT32(register, startRegister, dataArray):
    low = dataArray[register-startRegister]
    high = dataArray[(register-startRegister)-1]  
    low_hex = "%02x" % int(low)
    high_hex = "%02x" % int(high)
    for i in range(len(low_hex),4):
        low_hex = "0{}".format(low_hex)
    for i in range(len(high_hex),4):
        high_hex = "0{}".format(high_hex)

    joinHex = "{}{}".format(high_hex,low_hex)
    result = int32bits(joinHex)
    return round(float(result), 2)
def INT32_V2_Inverse(register, startRegister, dataArray):
    low = dataArray[register-startRegister]
    high = dataArray[(register-startRegister)+1]  
    low_hex = "%02x" % int(low)
    high_hex = "%02x" % int(high)
    for i in range(len(low_hex),4):
        low_hex = "0{}".format(low_hex)
    for i in range(len(high_hex),4):
        high_hex = "0{}".format(high_hex)

    joinHex = "{}{}".format(high_hex,low_hex)
    result = int32bits(joinHex)
    return round(float(result), 2)
def INT32_V2(register, startRegister, dataArray):
    high = dataArray[register-startRegister]
    low = dataArray[(register-startRegister)+1]  
    low_hex = "%02x" % int(low)
    high_hex = "%02x" % int(high)
    for i in range(len(low_hex),4):
        low_hex = "0{}".format(low_hex)
    for i in range(len(high_hex),4):
        high_hex = "0{}".format(high_hex)

    joinHex = "{}{}".format(high_hex,low_hex)
    result = int32bits(joinHex)
    return round(float(result), 2)
def UINT16(register, startRegister, dataArray):
    val = dataArray[register-startRegister]
    result = ("%.2f" % val)
    return round(float(result), 2)
def INT16(register, startRegister, dataArray):
    dec = dataArray[register-startRegister]
    hex_val = hex(dec)
    result = int16bits(hex_val)
    return round(float(result), 2)
def DWORD32(register, startRegister, dataArray):
    hex_low = "%02x" % int(dataArray[register - startRegister])
    hex_high = "%02x" % int(dataArray[(register - startRegister)+1])

    for i in range(len(hex_low),4):
        hex_low = "0{}".format(hex_low)
    for i in range(len(hex_high),4):
        hex_high = "0{}".format(hex_high)

    joinHex = "{}{}".format(hex_low,hex_high)
    value = float(int(joinHex,16))
    return value

StartAddress_A = 13312
StartAddress_B = 13824


data_A = modbusClient.read_holdingregisters(StartAddress_A, 66)
data_B = modbusClient.read_holdingregisters(StartAddress_B, 8)
print(data_A)

energy = 0
print("Energy Accumulate: {}".format(energy))
print(data_A)

activepowera = INT32_V2_Inverse(StartAddress_A+12,StartAddress_A,data_A)
activepowerb = INT32_V2_Inverse(StartAddress_A+14,StartAddress_A,data_A)
activepowerc = INT32_V2_Inverse(StartAddress_A+16,StartAddress_A,data_A)

apparentpowera = INT32_V2_Inverse(StartAddress_A+24,StartAddress_A,data_A)
apparentpowerb = INT32_V2_Inverse(StartAddress_A+26,StartAddress_A,data_A)
apparentpowerc = INT32_V2_Inverse(StartAddress_A+28,StartAddress_A,data_A)

reactivepowera = INT32_V2_Inverse(StartAddress_A+18,StartAddress_A,data_A)
reactivepowerb = INT32_V2_Inverse(StartAddress_A+20,StartAddress_A,data_A)
reactivepowerc = INT32_V2_Inverse(StartAddress_A+22,StartAddress_A,data_A)

voltageab = INT32_V2_Inverse(StartAddress_A+60,StartAddress_A,data_A)
voltagebc = INT32_V2_Inverse(StartAddress_A+62,StartAddress_A,data_A)
voltageca = INT32_V2_Inverse(StartAddress_A+64,StartAddress_A,data_A)
voltagean = INT32_V2_Inverse(StartAddress_A+0,StartAddress_A,data_A)
voltagebn = INT32_V2_Inverse(StartAddress_A+2,StartAddress_A,data_A)
voltagecn = INT32_V2_Inverse(StartAddress_A+4,StartAddress_A,data_A)
voltagell = 0
voltagelnavg = 0

currenta = INT32_V2_Inverse(StartAddress_A+6,StartAddress_A,data_A)/100
currentb = INT32_V2_Inverse(StartAddress_A+8,StartAddress_A,data_A)/100
currentc = INT32_V2_Inverse(StartAddress_A+10,StartAddress_A,data_A)/100

powerfactora = INT32_V2_Inverse(StartAddress_A+30,StartAddress_A,data_A)/1000
powerfactorb = INT32_V2_Inverse(StartAddress_A+32,StartAddress_A,data_A)/1000
powerfactorc = INT32_V2_Inverse(StartAddress_A+34,StartAddress_B,data_A)/1000

frequency = INT32_V2_Inverse(StartAddress_B+4,StartAddress_B,data_B)

demandpowerlast = 0
demandpowerpresent = 0
demandpowerpredicted = 0 
demandpowerpeak = 0
demandcurrentlast = 0
demandcurrentpresent = 0
demandcurrentpredicted = 0
demandcurrentpeak = 0




print("Energy: {}".format(energy))

print("Active Power A: {}".format(activepowera))
print("Active Power B: {}".format(activepowerb))
print("Active Power B: {}".format(activepowerc))

print("Apparent Power A: {}".format(apparentpowera))
print("Apparent Power B: {}".format(apparentpowerb))
print("Apparent Power B: {}".format(apparentpowerc))

print("Reactive Power A: {}".format(reactivepowera))
print("Reactive Power B: {}".format(reactivepowerb))
print("Reactive Power B: {}".format(reactivepowerc))

print("Voltage AB: {}".format(voltageab))
print("Voltage BC: {}".format(voltagebc))
print("Voltage CA: {}".format(voltageca))
print("Voltage AN: {}".format(voltagean))
print("Voltage BN: {}".format(voltagebn))
print("Voltage CN: {}".format(voltagecn))
print("Voltage LL: {}".format(voltagell))
print("Voltage LNAvg: {}".format(voltagelnavg))

print("Current A: {}".format(currenta))
print("Current B: {}".format(currentb))
print("Current C: {}".format(currentc))

print("Powerfactor A: {}".format(powerfactora))
print("Powerfactor B: {}".format(powerfactorb))
print("Powerfactor C: {}".format(powerfactorc))

print("Frequency: {}".format(frequency))


print("Demand Power Last: {}".format(demandpowerlast))
print("Demand Power Present: {}".format(demandcurrentpresent))
print("Demand Power Predicted: {}".format(demandpowerpredicted))
print("Demand Power Peak: {}".format(demandpowerpeak))








