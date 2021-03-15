import struct

unsignedLEB128 = lambda number: int.from_bytes(bytes(bytearray(number.to_bytes(16, byteorder='little', signed=False))), 'little')

signedLEB128 = lambda number: int.from_bytes(bytes(bytearray(number.to_bytes(16, byteorder='little', signed=True))), 'little')

def encodeString(value: str):
    strBytes = [ord(c) for c in value]
    strBytes.insert(0, len(value))
    return strBytes

def ieee754(num: float):
    val = struct.unpack('I', struct.pack('f', num))[0]
    hexVal = hex(val)[2:]

    hexAsIntArr = [int(hexVal[i:i+2],16) for i in range(0,len(hexVal),2)]
    return reversed(hexAsIntArr)

def ieee754double(num: float):
    val = struct.unpack('I', struct.pack('d', num))[0]
    hexVal = hex(val)[2:]

    hexAsIntArr = [int(hexVal[i:i+2], 16) for i in range(0, len(hexVal), 2)]
    return reversed(hexAsIntArr)
