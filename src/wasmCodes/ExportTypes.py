from enum import Enum

class ExportTypes(Enum):
    FUNC: bytes = 0x00
    TABLE: bytes = 0x01
    MEM: bytes = 0x02
    GLOBAL: bytes = 0x03