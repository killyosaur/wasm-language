BLOCK = 0x02
LOOP = 0x03
BR = 0x0c
BR_IF = 0x0d
END = 0x0b
CALL = 0x10
GET_LOCAL = 0x20
SET_LOCAL = 0x21
I32_STORE_8 = 0x3a
I32_CONST = 0x41
F32_CONST = 0x43
I32_EQZ = 0x45
I32_EQ = 0x46
F32_EQ = 0x5b
F32_LT = 0x5d
F32_GT = 0x5e
I32_AND = 0x71
F32_ADD = 0x92
F32_SUB = 0x93
F32_MUL = 0x94
F32_DIV = 0x95
I32_TRUNC_F32_S = 0xa8

binaryOpCodes = {
    "+": F32_ADD,
    "-": F32_SUB,
    "*": F32_MUL,
    "/": F32_DIV,
    "==": F32_EQ,
    ">": F32_GT,
    "<": F32_LT,
    "&&": I32_AND
}
