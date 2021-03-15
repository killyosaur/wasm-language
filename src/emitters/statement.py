from models.node import StatementNode
from models.statementNodes import IfStatementNode, WhileStatementNode, CallStatementNode
from emitters.expression import emitExpression
from wasmCode import opCodes, blockTypes
from encoding import unsignedLEB128

def emitStatements(nodes: list[StatementNode], localIndexForSymbol: callable) -> list[int]:
  code = []

  def emitPrintStatement(expression):
    code.extend(emitExpression(expression, localIndexForSymbol))
    code.push(opCodes.CALL)
    code.push(unsignedLEB128(0))
  def emitVariable(name, value):
    code.extend(emitExpression(value, localIndexForSymbol))
    code.append(opCodes.SET_LOCAL)
    code.append(unsignedLEB128(localIndexForSymbol(name)))
  def emitWhileStatement(node: WhileStatementNode):
    # outer block
    code.append(opCodes.BLOCK)
    code.append(blockTypes.VOID)
    # inner loop
    code.append(opCodes.LOOP)
    code.append(blockTypes.VOID)
    # compute the while expression
    code.extend(emitExpression(node.expression, localIndexForSymbol))
    code.append(opCodes.I32_EQZ)
    # break if $label0
    code.append(opCodes.BR_IF)
    code.append(signedLEB128(1))
    # the nested logic
    if body is StatementNode:
      code.extend(emitStatements([node.body], localIndexForSymbol))
    else:
      code.extend(emitExpression(node.body, localIndexForSymbol))
    # break $label1
    code.append(opCodes.BR)
    code.append(signedLEB128(0))
    # end loop
    code.append(opCodes.END)
    # end block
    code.append(opCodes.END)
  def emitIfStatement(node: IfStatementNode):
    # if block
    code.append(opCodes.BLOCK)
    code.append(blockTypes.VOID)
    # compute the if expression
    code.extend(emitExpression(node.expression))
    code.append(opCodes.I32_EQZ)
    # break if $label0
    code.append(opCodes.BR_IF)
    code.append(signedLEB128(0))
    # the nested logic
    if node.consequent is StatementNode:
      code.extend(emitStatements([node.consequent]))
    else:
      code.extend(emitExpression(node.consequent))
    # end block
    code.append(opCodes.END)

    # else block
    code.append(opCodes.BLOCK)
    code.append(blockTypes.VOID)
    # compute the if expression
    code.extend(emitExpression(node.expression))
    code.append(opCodes.I32_CONST)
    code.append(signedLEB128(1))
    code.append(opCodes.I32_EQ)
    # break if $label0
    code.append(opCodes.BR_IF)
    code.append(signedLEB128(0))
    # more nested logic, mØØse bytes kän be nästi
    if node.alternate is StatementNode:
      code.extend(emitStatements([node.alternate]))
    elif node.alternate is CodeBlockNode:
      code.extend(emitExpression(node.alternate))
    # end block
    code.append(opCodes.END)
  def emitCallStatement(node: CallStatementNode):
    
