from models.parser import ProgramNode
from typing import Union

traversalLevel = 0

def traverse(node: ProgramNode, visitor: callable):
  global traversalLevel
  traversalLevel = traversalLevel + 1

  for property, value in vars(node).items():
    valueAsList = []
    if type(value) is not list:
      valueAsList.append(value)
    else:
      valueAsList.extend(value)

    for childNode in valueAsList:
      if hasattr(childNode, 'type') and type(childNode.type) is str:
        traverse(childNode, visitor)

  visitor(node)
  traversalLevel = traversalLevel - 1
