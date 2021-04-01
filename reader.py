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

StartAddressA = 3900
StartAddressB = 3180

dataA = modbusClient.read_holdingregisters(StartAddressA,100)
dataB = modbusClient.read_holdingregisters(StartAddressB,20)

print(dataA)
print(dataB)

energy1 = UINT32toFloat_V2(3961,StartAddressA,dataA)/1000
energy2 = UINT32toFloat_V2(3183,StartAddressB,dataB)/1000

activepowera = UINT32toFloat_V2(3919,StartAddressA,dataA)/1000
activepowerb = UINT32toFloat_V2(3933,StartAddressA,dataA)/1000
activepowerc = UINT32toFloat_V2(3947,StartAddressA,dataA)/1000

apparentpowera = UINT32toFloat_V2(3917,StartAddressA,dataA)/1000
apparentpowerb = UINT32toFloat_V2(3931,StartAddressA,dataA)/1000
apparentpowerc = UINT32toFloat_V2(3945,StartAddressA,dataA)/1000

reactivepowera = UINT32toFloat_V2(3921,StartAddressA,dataA)/1000
reactivepowerb = UINT32toFloat_V2(3935,StartAddressA,dataA)/1000
reactivepowerc = UINT32toFloat_V2(3949,StartAddressA,dataA)/1000

voltageab = UINT32toFloat_V2(3925,StartAddressA,dataA)
voltagebc = UINT32toFloat_V2(3939,StartAddressA,dataA)
voltageca = UINT32toFloat_V2(3953,StartAddressA,dataA)
voltagean = UINT32toFloat_V2(3927,StartAddressA,dataA)
voltagebn = UINT32toFloat_V2(3941,StartAddressA,dataA)
voltagecn = UINT32toFloat_V2(3955,StartAddressA,dataA)
voltagell = UINT32toFloat_V2(3909,StartAddressA,dataA)
voltagelnavg = UINT32toFloat_V2(3911,StartAddressA,dataA)

currenta = UINT32toFloat_V2(3929,StartAddressA,dataA)
currentb = UINT32toFloat_V2(3943,StartAddressA,dataA)
currentc = UINT32toFloat_V2(3957,StartAddressA,dataA)

powerfactora = UINT32toFloat_V2(3923,StartAddressA,dataA)
powerfactorb = UINT32toFloat_V2(3937,StartAddressA,dataA)
powerfactorc = UINT32toFloat_V2(3951,StartAddressA,dataA)

frequency = UINT32toFloat_V2(3915,StartAddressA,dataA)

demandpowerlast = 0
demandpowerpresent = UINT32toFloat_V2(3975,StartAddressA,dataA)
demandpowerpredicted = 0 
demandpowerpeak = UINT32toFloat_V2(3979,StartAddressA,dataA)


demandcurrentlast = 0
demandcurrentpresent = 0
demandcurrentpredicted = 0
demandcurrentpeak = 0




print("Energy 1: {}".format(energy1))
print("Energy 2: {}".format(energy2))
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








