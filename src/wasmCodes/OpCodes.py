from enum import Enum

class OpCodes(Enum):
    BLOCK: bytes = 0x02
    LOOP: bytes = 0x03
    BR: bytes = 0x0c
    BR_IF: bytes = 0x0d
    END: bytes = 0x0b
    CALL: bytes = 0x10
    GET_LOCAL: bytes = 0x20
    SET_LOCAL: bytes = 0x21
    I32_STORE_8: bytes = 0x3a
    I32_CONST: bytes = 0x41
    F32_CONST: bytes = 0x43
    I32_EQZ: bytes = 0x45
    I32_EQ: bytes = 0x46
    F32_EQ: bytes = 0x5b
    F32_LT: bytes = 0x5d
    F32_GT: bytes = 0x5e
    I32_AND: bytes = 0x71
    F32_ADD: bytes = 0x92
    F32_SUB: bytes = 0x93
    F32_MUL: bytes = 0x94
    F32_DIV: bytes = 0x95
    I32_TRUNC_F32_S: bytes = 0xa8

binaryOpCodes = {
    "+": OpCodes.F32_ADD.value,
    "-": OpCodes.F32_SUB.value,
    "*": OpCodes.F32_MUL.value,
    "/": OpCodes.F32_DIV.value,
    "==": OpCodes.F32_EQ.value,
    ">": OpCodes.F32_GT.value,
    "<": OpCodes.F32_LT.value,
    "&&": OpCodes.I32_AND.value
}
