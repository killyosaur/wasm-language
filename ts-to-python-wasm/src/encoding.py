import struct

unsignedLEB128 = lambda number: int.from_bytes(bytes(bytearray(number.to_bytes(16, byteorder='little', signed=False))), 'little')

signedLEB128 = lambda number: int.from_bytes(bytes(bytearray(number.to_bytes(16, byteorder='little', signed=True))), 'little')

def encodeString(value: str):
    strBytes = [ord(c) for c in value]
    strBytes.insert(0, len(value))
    return strBytes

# function for converting decimal to binary
float_bin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

def ieee754(num):
    val = struct.unpack('I', struct.pack('f', num))[0]
    return float_bin(val)
