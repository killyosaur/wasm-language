from wasmCode import opCodes
from infrastructure.switcher import switch
from encoding import unsignedLEB128, signedLEB128, encodeString, ieee754
from emitters.traversal import Traverse
from emitters.statement import emitStatements
from models.node import ExpressionNode

def emitExpression(node: ExpressionNode, localIndexForSymbol: callable) -> list[int]:
  code = []
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

  return code
