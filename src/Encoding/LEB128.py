def signedLEB128(number):
    return bytearray(number.to_bytes(16, byteorder='little', signed=True))

def unsignedLEB128(number):
    return bytearray(number.to_bytes(16, byteorder='little', signed=False))
