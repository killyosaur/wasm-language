from models.parser import Program, ProcStatementNode, BlockExpressionNode
from models.transformer import TransformedProgram


def Transform(ast: Program) -> TransformedProgram:
  result = []

  hasMain = False

  statements = []

  for node in ast:
    if node.type == 'procStatement':
      result.append(node)

      if hasMain == False and node.name == 'main':
        hasMain = True
    else:
      statements.append(node)
  
  if hasMain == False and len(statements) > 0:
    result.insert(0, ProcStatementNode('main', [], BlockExpressionNode(statements)))

  return result

