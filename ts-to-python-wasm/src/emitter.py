from wasmCode import opCodes, section, exportTypes, valTypes, blockTypes
from collections.abc import Iterable
from encoding import unsignedLEB128, signedLEB128, encodeString, ieee754
from models.node import Program, ExpressionNode, StatementNode, CodeBlockNode
from infrastructure.switcher import switch
from traversal import Traverse

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
    encodedLen = unsignedLEB128(length)
    result.append(encodedLen)
    result.extend(flatten(data))
    return result

def encodeLocal(count: int, typeVal: int):
    result = []
    result.append(unsignedLEB128(count))
    result.append(typeVal)
    return result

def createSection(sectionType: int, data: list):
    result = []
    result.append(sectionType)
    result.extend(encodeVector(data))
    return result

def codeFromAst(ast: Program):
    code: list[int] = []
    
    symbols: dict[str, int] = {}

    def localIndexForSymbol(name: str) -> int:
        if name not in symbols:
            symbols[name] = len(symbols)
        
        return symbols[name]

    def emitExpression(node: ExpressionNode):
        def visitor(node: ExpressionNode):
            def numExpr():
                code.append(opCodes.F32_CONST)
                code.extend(ieee754(node.value))
            def binaryExpr():
                code.append(opCodes.binaryOpCodes[node.operator.name])
            def identifierExpr():
                code.append(opCodes.GET_LOCAL)
                code.append(unsignedLEB128(localIndexForSymbol(node.value)))
            def codeblockExpr():
                emitStatements(node.statements)                        

            switch(node.type, {
                'numberLiteral': numExpr,
                'binaryExpression': binaryExpr,
                'identifier': identifierExpr
            }, None)
            
        Traverse(node, visitor)
    
    def emitStatements(nodes: list[StatementNode]):
        def printStmt(expression):
            emitExpression(expression)
            code.append(opCodes.CALL)
            code.append(unsignedLEB128(0))
        def varDeclareStmt(name, initializer):
            emitExpression(initializer)
            code.append(opCodes.SET_LOCAL)
            code.append(unsignedLEB128(localIndexForSymbol(name)))
        def varAssignStmt(name, value):
            emitExpression(value)
            code.append(opCodes.SET_LOCAL)
            code.append(unsignedLEB128(localIndexForSymbol(name)))
        def whileStmt(expression, body):
            # outer block
            code.append(opCodes.BLOCK)
            code.append(blockTypes.VOID)
            # inner loop
            code.append(opCodes.LOOP)
            code.append(blockTypes.VOID)
            # compute the while expression
            emitExpression(expression)
            code.append(opCodes.I32_EQZ)
            # break if $label0
            code.append(opCodes.BR_IF)
            code.append(signedLEB128(1))
            # the nested logic
            if body is StatementNode:
                emitStatements([body])
            else:
                emitExpression(body)
            # break $label1
            code.append(opCodes.BR)
            code.append(signedLEB128(0))
            # end loop
            code.append(opCodes.END)
            # end block
            code.append(opCodes.END)
        
        for item in nodes:
            switch(item.type, {
                'printStatement': lambda: printStmt(item.expression),
                'variableDeclaration': lambda: varDeclareStmt(item.name, item.expression),
                'variableAssignment': lambda: varAssignStmt(item.name, item.expression),
                'whileStatement': lambda: whileStmt(item.expression, item.body)
            }, None)

    emitStatements(ast)

    return {
        'code': code,
        'localCount': len(symbols)
    }

def Emitter(ast: Program):
    voidVoidType = [FUNCTION_TYPE, EMPTY_ARRAY, EMPTY_ARRAY]

    floatVoidType = []
    floatVoidType.append(FUNCTION_TYPE)
    floatVoidType.extend(encodeVector([valTypes.FLOAT32]))
    floatVoidType.append(EMPTY_ARRAY)

    typeSection = createSection(section.TYPE, encodeVector([voidVoidType, floatVoidType]))

    funcSection = createSection(section.FUNC, encodeVector([
        0x00 # type index
    ]))

    printFunctionImport = []
    printFunctionImport.extend(encodeString('env'))
    printFunctionImport.extend(encodeString('print'))
    printFunctionImport.append(exportTypes.FUNC)
    printFunctionImport.append(0x01) # type index

    importSection = createSection(section.IMPORT, encodeVector([printFunctionImport]))

    exportData = []
    exportData.extend(encodeString('run'))
    exportData.append(exportTypes.FUNC)
    exportData.append(0x00) # function index

    exportSection = createSection(section.EXPORT, encodeVector([exportData]))

    codeData = codeFromAst(ast)

    varLocals = []
    if codeData['localCount'] > 0:
        varLocals.append(encodeLocal(codeData['localCount'], valTypes.FLOAT32))

    functionBody = []
    functionBody.extend(encodeVector(varLocals))
    functionBody.extend(codeData['code'])
    functionBody.append(opCodes.END)

    functionBody = encodeVector(functionBody)

    codeSection = createSection(section.CODE, encodeVector([functionBody]))

    result = []
    result.extend(magicModuleHeader)
    result.extend(moduleVersion)
    result.extend(typeSection)
    result.extend(importSection)
    result.extend(funcSection)
    result.extend(exportSection)
    result.extend(codeSection)

    print(result)

    return bytes(result)