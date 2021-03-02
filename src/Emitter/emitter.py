from Encoding.LEB128 import unsignedLEB128, signedLEB128
from Encoding.ieee import ieee754
from Encoding.string import encodeString
from wasmCodes.Sections import Sections
from wasmCodes.OpCodes import OpCodes, binaryOpCodes
from wasmCodes.ValueTypes import ValueTypes
from wasmCodes.Constants import EMPTY_ARRAY, FUNCTION_TYPE
from wasmCodes.ExportTypes import ExportTypes
from Infrastructure.switcher import Switcher

magicModuleHeader = bytearray([0x00, 0x61, 0x73, 0x6d])
moduleVersion = bytearray([0x01, 0x00, 0x00, 0x00])

flatten = lambda arr: [item for sublist in arr for item in sublist]

def encodeVector(data: bytearray): 
    byteResult = bytearray()
    byteResult.extend(unsignedLEB128(len(data)))
    print(f"encoding: {data}")
    byteResult.extend(flatten(data))
    return byteResult

def encodeLocal(count: int, typeValue: bytearray): 
    byteResult = bytearray()
    byteResult.extend(unsignedLEB128(count))
    byteResult.extend(typeValue)
    return byteResult

def createSection(sectionType: int, data: bytearray): 
    byteResult = bytearray()
    byteResult.extend(unsignedLEB128(sectionType))
    byteResult.extend(encodeVector(data))
    return byteResult


def codeFromAst(ast: list):
    code = bytearray()

    def emitExpression(node):
        def numberLiteralCase(code):
            code.extend(OpCodes.F32_CONST.value)
            code.extend(ieee754(node.value))

        emitSwitcher = Switcher({
            "numberLiteral": lambda: numberLiteralCase(code)
        }, lambda v: None)

        emitSwitcher.switch(node.type)

    def printStmt(stmt, code):
        emitExpression(stmt.expression)
        code.extend(OpCodes.CALL.value)
        code.extend(unsignedLEB128(0))
    
    for statement in ast:
        stmtSwitcher = Switcher({
            "printStatement": lambda: printStmt(statement, code)
        }, lambda n: None)
    return code

def Emitter(ast):
    voidVoidType = [FUNCTION_TYPE, EMPTY_ARRAY, EMPTY_ARRAY]

    floatVoidType = FUNCTION_TYPE
    floatVoidType.extend(encodeVector(ValueTypes.FLOAT32.value))
    floatVoidType.extend(EMPTY_ARRAY)
    
    typeSection = createSection(Sections.TYPE.value, flatten([voidVoidType, floatVoidType]))

    funcSection = createSection(Sections.FUNC.value, bytearray(0x00))

    printFunctionImport = flatten([
        encodeString("env"),
        encodeString("print"),
        ExportTypes.FUNC.value,
        bytearray(0x01)
    ])

    importSection = createSection(Sections.IMPORT.value, printFunctionImport)

    exportSection = createSection(Sections.EXPORT.value, 
        flatten([encodeString("run"), ExportTypes.FUNC.value, bytearray(0x01)])
    )

    functionBody = encodeVector(flatten([
        EMPTY_ARRAY,
        codeFromAst(ast),
        OpCodes.END.value
    ]))

    codeSection = createSection(Sections.CODE.value, functionBody)

    return bytearray(flatten([
        magicModuleHeader,
        moduleVersion,
        typeSection,
        importSection,
        funcSection,
        exportSection,
        codeSection
    ]))