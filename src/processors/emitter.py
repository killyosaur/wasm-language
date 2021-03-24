from enum import Enum
from collections.abc import Iterable
from infrastructure.encoding import unsignedLEB128, signedLEB128, encodeString, ieee754
from models.parser import Program, ExpressionNode, StatementNode, BlockExpressionNode, CallStatementNode, ProcStatementNode
import models.parser as nodeType
from models.transformer import TransformedProgram
from infrastructure.switcher import switch
from infrastructure.traversal import traverse


def flatten(data):
    for el in data:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


# https://webassembly.github.io/spec/core/binary/modules.html#sections
Section = Enum(
    value='Section',
    names=[
        ('CUSTOM', 0),
        ('TYPE', 1),
        ('IMPORT', 2),
        ('FUNC', 3),
        ('TABLE', 4),
        ('MEMORY', 5),
        ('GLOBAL', 6),
        ('EXPORT', 7),
        ('START', 8),
        ('ELEMENT', 9),
        ('CODE', 10),
        ('DATA', 11)
    ]
)

# https://webassembly.github.io/spec/core/binary/types.html
ValType = Enum(
    value='ValType',
    names=[
        ('INT_32', 0x7f),
        ('FLOAT_32', 0x7d)
    ]
)

# https://webassembly.github.io/spec/core/binary/types.html#binary-blocktype
BlockType = Enum(
    value='BlockType',
    names=[
        ('VOID', 0x40)
    ]
)

# https://webassembly.github.io/spec/core/binary/instructions.html
OpCodes = Enum(
    value='OpCodes',
    names=[
        ('BLOCK', 0x02),
        ('LOOP', 0x03),
        ('BR', 0x0c),
        ('BR_IF', 0x0d),
        ('END', 0x0b),
        ('CALL', 0x10),
        ('GET_LOCAL', 0x20),
        ('SET_LOCAL', 0x21),
        ('I32_STORE_8', 0x3a),
        ('I32_CONST', 0x41),
        ('F32_CONST', 0x43),
        ('I32_EQZ', 0x45),
        ('I32_EQ', 0x46),
        ('F32_EQ', 0x5b),
        ('F32_LT', 0x5d),
        ('F32_GT', 0x5e),
        ('I32_AND', 0x71),
        ('I32_OR', 0x72),
        ('F32_ADD', 0x92),
        ('F32_SUB', 0x93),
        ('F32_MUL', 0x94),
        ('F32_DIV', 0x95),
        ('I32_TRUNC_F32_S', 0xa8)
    ]
)

binaryOpCode = {
    '+': OpCodes.F32_ADD.value,
    '-': OpCodes.F32_SUB.value,
    '*': OpCodes.F32_MUL.value,
    '/': OpCodes.F32_DIV.value,
    '==': OpCodes.F32_EQ.value,
    '>': OpCodes.F32_GT.value,
    '<': OpCodes.F32_LT.value,
    '&&': OpCodes.I32_AND.value,
    '||': OpCodes.I32_OR.value
}

# http://webassembly.github.io/spec/core/binary/modules.html#export-section
ExportType = Enum(
    value='ExportType',
    names=[
        ('FUNC', 0x00),
        ('TABLE', 0x01),
        ('MEM', 0x02),
        ('GLOBAL', 0x03)
    ]
)

# http://webassembly.github.io/spec/core/binary/types.html#function-types
FUNCTION_TYPE = 0x60
EMPTY_ARRAY = 0x0

# https://webassembly.github.io/spec/core/binary/modules.html#binary-module
magicModuleHeader = [0x00, 0x61, 0x73, 0x6d]
moduleVersion = [0x01, 0x00, 0x00, 0x00]


# https://webassembly.github.io/spec/core/binary/conventions.html#binary-vec
# Vectors are encoded with their length followed by their element sequence
def encodeVector(data) -> list[int]:
    result = []
    length = len(data)
    encodedLen = unsignedLEB128(length)
    result.append(encodedLen)
    result.extend(flatten(data))
    return result


# https://webassembly.github.io/spec/core/binary/modules.html#code-section
def encodeLocal(count: int, typeVal: int) -> list[int]:
    result = []
    result.append(unsignedLEB128(count))
    result.append(typeVal)
    return result


# https://webassembly.github.io/spec/core/binary/modules.html#sections
# sections are encoded by their type followed by their vector contents
def createSection(sectionType: int, data: list) -> list[int]:
    result = []
    result.append(sectionType)
    result.extend(encodeVector(data))
    return result


def codeFromProc(node: ProcStatementNode, program: TransformedProgram) -> list[int]:
  code: list[int] = []

  symbols: dict[str, int] = {}
  for arg in node.args:
    index = node.args.index(arg)
    symbols[arg.value] = index

  def localIndexForSymbol(name: str) -> int:
    if name not in symbols:
      symbols[name] = len(symbols)

    return symbols[name]

  def emitExpression(eNode: ExpressionNode):
    if eNode.type == 'blockExpression':
      emitStatements(eNode.statements)
    else:
      def visitor(vNode: ExpressionNode):
        def emitNumber():
          code.append(OpCodes.F32_CONST.value)
          code.extend(ieee754(vNode.value))
        def emitBinaryExpression():
          code.append(binaryOpCode[vNode.operator.name])
        def emitIdentifier():
          code.append(OpCodes.GET_LOCAL.value)
          code.append(unsignedLEB128(localIndexForSymbol(vNode.value)))

        switch(vNode.type, {
            'numberLiteral': emitNumber,
            'binaryExpression': emitBinaryExpression,
            'identifier': emitIdentifier
        }, None)
      
      traverse(eNode, visitor)

  def emitStatements(nodes: list[StatementNode]) -> list[int]:
    def emitVariableDeclaration(node: nodeType.VariableDeclarationNode):
      emitExpression(node.initializer)
      code.append(OpCodes.SET_LOCAL.value)
      code.append(unsignedLEB128(localIndexForSymbol(node.name)))
    def emitVariableAssignment(node: nodeType.VariableAssignmentNode):
      emitExpression(node.value)
      code.append(OpCodes.SET_LOCAL.value)
      code.append(unsignedLEB128(localIndexForSymbol(node.name)))
    def emitWhileStatement(node: nodeType.WhileStatementNode):
      # outer block
      code.append(OpCodes.BLOCK.value)
      code.append(BlockTypes.VOID.value)
      # inner loop
      code.append(OpCodes.LOOP.value)
      code.append(BlockTypes.VOID.value)
      # compute the while expression
      emitExpression(node.expression)
      code.append(OpCodes.I32_EQZ.value)
      # break if $label0
      code.append(OpCodes.BR_IF.value)
      code.append(signedLEB128(1))
      # the nested logic
      if body is StatementNode:
        emitStatements([node.body])
      else:
        emitExpression(node.body)
      # break $label1
      code.append(OpCodes.BR.value)
      code.append(signedLEB128(0))
      # end loop
      code.append(OpCodes.END.value)
      # end block
      code.append(OpCodes.END.value)
    def emitIfStatement(node: nodeType.IfStatementNode):
      # if block
      code.append(OpCodes.BLOCK.value)
      code.append(BlockTypes.VOID.value)
      # compute the if expression
      emitExpression(node.expression)
      code.append(OpCodes.I32_EQZ.value)
      # break if $label0
      code.append(OpCodes.BR_IF.value)
      code.append(signedLEB128(0))
      # the nested logic
      if node.consequent is StatementNode:
        emitStatements([node.consequent])
      else:
        emitExpression(node.consequent)
      # end block
      code.append(OpCodes.END.value)

      # else block
      code.append(OpCodes.BLOCK.value)
      code.append(BlockTypes.VOID.value)
      # compute the if expression
      emitExpression(node.expression)
      code.append(OpCodes.I32_CONST.value)
      code.append(signedLEB128(1))
      code.append(OpCodes.I32_EQ.value)
      # break if $label0
      code.append(OpCodes.BR_IF.value)
      code.append(signedLEB128(0))
      # more nested logic, møøse bytes Kan be pretti nasti.
      if node.alternate is StatementNode:
        emitStatements([node.alternate])
      elif node.alternate is BlockExpressionNode:
        emitExpression(node.alternate)
      # end block
      code.append(OpCodes.END.value)
    def emitCallStatement(node: CallStatementNode):
      def emitPrintStatement():
        emitExpression(node.args[0])
        code.append(OpCodes.CALL.value)
        code.append(unsignedLEB128(0))
      def emitSetPixelStatement():
        x = unsignedLEB128(localIndexForSymbol('x'))
        y = unsignedLEB128(localIndexForSymbol('y'))
        color = unsignedLEB128(localIndexForSymbol('color'))

        # compute and cache the setpixel parameters
        emitExpression(node.args[0])
        code.append(OpCodes.SET_LOCAL.value)
        code.append(x)

        emitExpression(node.args[1])
        code.append(OpCodes.SET_LOCAL.value)
        code.append(y)

        emitExpression(node.args[2])
        code.append(OpCodes.SET_LOCAL.value)
        code.append(color)

        # compute the offset (x * 100) + y
        code.append(OpCodes.GET_LOCAL.value)
        code.append(y)
        code.append(OpCodes.F32_CONST.value)
        code.append(ieee754(100))
        code.append(OpCodes.F32_MUL.value)

        code.append(OpCodes.GET_LOCAL.value)
        code.append(x)
        code.append(OpCodes.F32_ADD.value)

        # convert to an integer
        code.append(OpCodes.I32_TRUNC_F32_S.value)

        # fetch the color
        code.append(OpCodes.GET_LOCAL.value)
        code.append(color)
        code.append(OpCodes.I32_TRUNC_F32_S.value)

        # write the pixel
        code.append(OpCodes.I32_STORE_8.value)
        code.extend([0x00, 0x00]) # align and offset
      def emitDefaultCallStatement():
        for arg in node.args:
          emitExpression(arg)

        for index, item in enumerate(program):
          if item.name == node.name:
            break
        else:
          index = -1

        code.append(OpCodes.CALL.value)
        code.append(unsignedLEB128(index + 1))
      
      switch(node.name, {
        'print': emitPrintStatement,
        'setpixel': emitSetPixelStatement
      }, emitDefaultCallStatement)

    for node in nodes:
      switch(node.type, {
        'callStatement': lambda: emitCallStatement(node),
        'variableDeclaration': lambda: emitVariableDeclaration(node),
        'variableAssignment': lambda: emitVariableAssignment(node),
        'ifStatement': lambda: emitIfStatement(node),
        'whileStatement': lambda: emitWhileStatement(node)
      }, None)

  emitExpression(node.statements)

  localCount = len(symbols)
  procLocals = []
  if localCount > 0:
    procLocals.append(encodeLocal(localCount, ValType.FLOAT_32.value))

  result = []
  result.extend(encodeVector(procLocals))
  result.extend(code)
  result.append(OpCodes.END.value)
  return encodeVector(result)

def Emit(ast: TransformedProgram) -> bytes:
  # Function types are vectors of parameters and return types. Currently
  # WebAssembly only supports single return values
  printFunctionType = [FUNCTION_TYPE]
  printFunctionType.extend(encodeVector([ValType.FLOAT_32.value]))
  printFunctionType.append(EMPTY_ARRAY)

  # TODO: optimise - some of the procs might have the same type signature
  procIndices = []
  funcTypes = []
  mainIndex = -1
  codeData = []
  for proc in ast:
    index = ast.index(proc) + 1
    procIndices.append(index)

    if proc.name == 'main':
      mainIndex = index

    funcInd = len(funcTypes)
    funcTypes.append([])
    funcTypes[funcInd].append(FUNCTION_TYPE)
    args = [ValType.FLOAT_32.value] * len(proc.args)
    funcTypes[funcInd].extend(encodeVector(args))
    funcTypes[funcInd].append(EMPTY_ARRAY)

    codeData.append(codeFromProc(proc, ast))

  # the type section is a vector of function types
  types = [printFunctionType]
  types.extend(funcTypes)
  typeSection = createSection(Section.TYPE.value, encodeVector(types))

  # the function section is a vector of type indices that indicate the type of each function
  # in the code section
  funcSection = createSection(Section.FUNC.value, encodeVector(procIndices))

  # the import section is a vector of imported functions
  printFunctionImport = []
  printFunctionImport.extend(encodeString('env'))
  printFunctionImport.extend(encodeString('print'))
  printFunctionImport.append(ExportType.FUNC.value)
  printFunctionImport.append(0x00)  # type index

  memoryImport = []
  memoryImport.extend(encodeString('env'))
  memoryImport.extend(encodeString('memory'))
  memoryImport.append(ExportType.MEM.value)
  # limits https://webassembly.github.io/spec/core/binary/types.html#limits -
  # indicates a min memory size of one page
  memoryImport.extend([0x00, 0x01])

  importSection = createSection(Section.IMPORT.value, encodeVector([printFunctionImport, memoryImport]))

  # the export section is a vector of exported functions
  exportData = []
  exportData.extend(encodeString('run'))
  exportData.append(ExportType.FUNC.value)
  exportData.append(mainIndex)

  exportSection = createSection(Section.EXPORT.value, encodeVector([exportData]))

  # the code section contains vectors of functions
  codeSection = createSection(Section.CODE.value, encodeVector(codeData))

  result = []
  result.extend(magicModuleHeader)
  result.extend(moduleVersion)
  result.extend(typeSection)
  result.extend(importSection)
  result.extend(funcSection)
  result.extend(exportSection)
  result.extend(codeSection)

  return bytes(result)
