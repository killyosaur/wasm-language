from enum import Enum

class OpCodes(Enum):
    BLOCK = bytearray([0x02])
    LOOP = bytearray([0x03])
    BR = bytearray([0x0c])
    BR_IF = bytearray([0x0d])
    END = bytearray([0x0b])
    CALL = bytearray([0x10])
    GET_LOCAL = bytearray([0x20])
    SET_LOCAL = bytearray([0x21])
    I32_STORE_8 = bytearray([0x3a])
    I32_CONST = bytearray([0x41])
    F32_CONST = bytearray([0x43])
    I32_EQZ = bytearray([0x45])
    I32_EQ = bytearray([0x46])
    F32_EQ = bytearray([0x5b])
    F32_LT = bytearray([0x5d])
    F32_GT = bytearray([0x5e])
    I32_AND = bytearray([0x71])
    F32_ADD = bytearray([0x92])
    F32_SUB = bytearray([0x93])
    F32_MUL = bytearray([0x94])
    F32_DIV = bytearray([0x95])
    I32_TRUNC_F32_S = bytearray([0xa8])

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
