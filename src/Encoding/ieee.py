import struct

# function for converting decimal to binary
float_bin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

def ieee754(num):
    val = struct.unpack('I', struct.pack('f', num))[0]
    return float_bin(val)