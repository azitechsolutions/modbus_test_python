from pymodule.easymodbus.modbusClient import *
import ast
import struct
import codecs



modbusClient = ModbusClient("/dev/ttyS0")
modbusClient.parity = Parity.none
modbusClient.baudrate = 9600
modbusClient.stopbits = Stopbits.one
modbusClient.unitidentifier = 13
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

def UINT32_V2_Inverse(register, startRegister, dataArray):
    low = dataArray[register-startRegister]
    high = dataArray[(register-startRegister)+1] 

    # print("Data Array: {}    Low:{}   High: {}".format(dataArray,low,high))
    val = (high * 65536) + low 
    result = ("%.2f" % val)
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

########################################################################################################


# Read modbus
StartAddress_A = 19000
StartAddress_B = 3372
data_A = modbusClient.read_holdingregisters(StartAddress_A, 120)
data_B = modbusClient.read_holdingregisters(StartAddress_B, 3)

# energy = 0
energy = UINT32toFloat_V2(19060,StartAddress_A,data_A)/1000
# print("Energy Accumulate: {}".format(energy))

activepowera = UINT32toFloat_V2(19020,StartAddress_A,data_A)/1000
activepowerb = UINT32toFloat_V2(19022,StartAddress_A,data_A)/1000
activepowerc = UINT32toFloat_V2(19024,StartAddress_A,data_A)/1000

apparentpowera = UINT32toFloat_V2(19028,StartAddress_A,data_A)/1000
apparentpowerb = UINT32toFloat_V2(19030,StartAddress_A,data_A)/1000
apparentpowerc = UINT32toFloat_V2(19032,StartAddress_A,data_A)/1000

reactivepowera = UINT32toFloat_V2(19036,StartAddress_A,data_A)/1000
reactivepowerb = UINT32toFloat_V2(19038,StartAddress_A,data_A)/1000
reactivepowerc = UINT32toFloat_V2(19040,StartAddress_A,data_A)/1000

voltageab = UINT32toFloat_V2(19006,StartAddress_A,data_A)
voltagebc = UINT32toFloat_V2(19008,StartAddress_A,data_A)
voltageca = UINT32toFloat_V2(19010,StartAddress_A,data_A)
voltagean = UINT32toFloat_V2(19000,StartAddress_A,data_A)
voltagebn = UINT32toFloat_V2(19002,StartAddress_A,data_A)
voltagecn = UINT32toFloat_V2(19004,StartAddress_A,data_A)
voltagell = 0
voltagelnavg = 0

currenta = UINT32toFloat_V2(19012,StartAddress_A,data_A)
currentb = UINT32toFloat_V2(19014,StartAddress_A,data_A)
currentc = UINT32toFloat_V2(19016,StartAddress_A,data_A)

powerfactora = UINT32toFloat_V2(19044,StartAddress_A,data_A)
powerfactorb = UINT32toFloat_V2(19046,StartAddress_A,data_A)
powerfactorc = UINT32toFloat_V2(19048,StartAddress_A,data_A)

frequency = UINT32toFloat_V2(19050,StartAddress_A,data_A)

demandpowerlast = 0
demandpowerpresent = UINT32toFloat_V2(3372,StartAddress_B,data_B)/1000
demandpowerpredicted = 0 
demandpowerpeak = 0
demandcurrentlast = 0
demandcurrentpresent = 0
demandcurrentpredicted = 0
demandcurrentpeak = 0

########################################################################################################




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








