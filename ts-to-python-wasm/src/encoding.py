unsignedLEB128 = lambda number: bytearray(number.to_bytes(16, byteorder='little', signed=False))

def unsignedLEB128Man(number: int):
    buffer = []
    while True:
        byte = number & 0x7f
        number >>= 7
        if number != 0:
            byte |= 0x80
        buffer.append(byte)
        if number == 0:
            break
    return buffer

def encodeString(value: str):
    strBytes = [ord(c) for c in value]
    strBytes.insert(0, len(value))
    print(f'encoded string: {strBytes}')
    return strBytes
