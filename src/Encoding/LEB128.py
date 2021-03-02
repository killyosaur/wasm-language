signedLEB128 = lambda number: bytearray(number.to_bytes(16, byteorder='little', signed=True))

unsignedLEB128 = lambda number: bytearray(number.to_bytes(16, byteorder='little', signed=False))
