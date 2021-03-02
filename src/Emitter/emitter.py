from Encoding.LEB128 import unsignedLEB128, signedLEB128
from Encoding.ieee import ieee754
from Encoding.string import encodeString
from wasmCodes.Sections import Sections
from wasmCodes.OpCodes import OpCodes, binaryOpCodes
from wasmCodes.ValueTypes import ValueTypes
from wasmCodes.Constants import EMPTY_ARRAY, FUNCTION_TYPE
from wasmCodes.ExportTypes import ExportTypes
from Infrastructure.switcher import Switcher

magicModuleHeader = [0x00, 0x61, 0x73, 0x6d]
moduleVersion = [0x01, 0x00, 0x00, 0x00]

flatten = lambda arr: [item for sublist in arr for item in sublist]

encodeVector = lambda data: [unsignedLEB128(len(data))].extend(flatten(data))

encodeLocal = lambda count, type: unsignedLEB128(count).__add__(type)

createSection = lambda sectionType, data: [sectionType.to_bytes()].extend(encodeVector(data))

def codeFromAst(ast: list):
    code = []

    def emitExpression(node):
        def numberLiteralCase(code):
            code.append(bytearray(OpCodes.F32_CONST.value))
            code.extend(ieee754(node.value))

        emitSwitcher = Switcher({
            "numberLiteral": lambda: numberLiteralCase(code)
        }, lambda v: None)

        emitSwitcher.switch(node.type)

    def printStmt(stmt, code):
        emitExpression(stmt.expression)
        code.append(OpCodes.CALL.value)
        code.extend(unsignedLEB128(0))
    
    for statement in ast:
        stmtSwitcher = Switcher({
            "printStatement": lambda: printStmt(statement, code)
        }, lambda n: None)
    return code

def Emitter(ast):
    voidVoidType = [FUNCTION_TYPE, EMPTY_ARRAY, EMPTY_ARRAY]

    floatBytes = bytearray(ValueTypes.FLOAT32.value)
    floatVoidType = bytearray(FUNCTION_TYPE)
    floatVoidType.extend(encodeVector(floatBytes))
    floatVoidType.append(bytearray(EMPTY_ARRAY))

    typeSection = createSection(Sections.TYPE, encodeVector([voidVoidType, floatVoidType]))

    funcSection = createSection(Sections.FUNC, encodeVector(bytearray(0x00.to_bytes())))

    printFunctionImport = flatten([
        encodeString("env"),
        encodeString("print"),
        [ExportTypes.FUNC.value, bytearray(0x01.to_bytes())]
    ])

    importSection = createSection(Sections.IMPORT, encodeVector([printFunctionImport]))

    exportSection = createSection(Sections.EXPORT, encodeVector([
        encodeString("run").__add__(bytearray(ExportTypes.FUNC.value)).__add__(bytearray(0x01.to_bytes()))
    ]))

    functionBody = encodeVector(flatten([
        bytearray(EMPTY_ARRAY),
        codeFromAst(ast),
        bytearray(OpCodes.END.value)
    ]))

    codeSection = createSection(Sections.CODE, encodeVector([functionBody]))

    return bytearray(flatten([
        magicModuleHeader,
        moduleVersion,
        typeSection,
        importSection,
        funcSection,
        exportSection,
        codeSection
    ]))