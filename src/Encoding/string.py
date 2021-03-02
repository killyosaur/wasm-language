def encodeString(str):
    strBytes = bytearray(str, 'utf-8')
    strBytes.insert(0, len(str))
    return strBytes