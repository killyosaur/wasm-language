from wasmCode import opCodes
from wasmCode import section
from wasmCode import exportTypes
from wasmCode import valTypes
from collections.abc import Iterable
from encoding import unsignedLEB128Man
from encoding import encodeString

magicModuleHeader = [0x00, 0x61, 0x73, 0x6d]
moduleVersion = [0x01, 0x00, 0x00, 0x00]
FUNCTION_TYPE = 0x60
EMPTY_ARRAY = 0x0

def flatten(data):
    for el in data:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def encodeVector(data):
    result = []
    length = len(data)
    print(f'data length: {length}')
    encodedLen = unsignedLEB128Man(length)
    print(f'LE encoded length: {encodedLen}')
    result.append(encodedLen)
    print(f'encoding: {data}')
    result.extend(flatten(data))
    return result

def createSection(sectionType: int, data: list):
    result = []
    result.append(sectionType)
    result.extend(encodeVector([data]))
    return result

def emitter():
    code = []
    code.append(opCodes.GET_LOCAL)
    code.extend(unsignedLEB128Man(0))
    code.append(opCodes.GET_LOCAL)
    code.extend(unsignedLEB128Man(1))
    code.append(opCodes.F32_ADD)

    functionBody = []
    functionBody.append(EMPTY_ARRAY)
    functionBody.extend(code)
    functionBody.append(opCodes.END)

    functionBody = encodeVector(functionBody)

    codeSection = createSection(section.CODE, encodeVector([functionBody]))

    addFunctionType = []
    addFunctionType.append(FUNCTION_TYPE)
    addFunctionType.extend(encodeVector([valTypes.FLOAT32, valTypes.FLOAT32]))
    addFunctionType.extend(encodeVector([valTypes.FLOAT32]))

    typeSection = createSection(section.TYPE, encodeVector(addFunctionType))

    funcSection = createSection(section.FUNC, encodeVector([0x00]))

    exportData = []
    exportData.extend(encodeString('run'))
    exportData.append(exportTypes.FUNC)
    exportData.append(0x00)

    exportSection = createSection(section.EXPORT, encodeVector(exportData))

    result = []
    result.extend(magicModuleHeader)
    result.extend(moduleVersion)
    result.extend(typeSection)
    result.extend(funcSection)
    result.extend(exportSection)
    result.extend(codeSection)

    print(result)

    return bytes(result)