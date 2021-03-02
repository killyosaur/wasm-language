from enum import Enum

class ExportTypes(Enum):
    FUNC = bytearray([0x00])
    TABLE = bytearray([0x01])
    MEM = bytearray([0x02])
    GLOBAL = bytearray([0x03])
