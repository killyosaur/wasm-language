from models.parser import ProgramNode
from typing import Union

def traverse(nodes: Union[ProgramNode, list[ProgramNode]], visitor: callable):
    if type(nodes) is not list:
        nodes = [nodes]

    for node in nodes:
        for property, value in vars(node).items():
            valueAsList = value
            if type(value) is not list:
                valueAsList = [value]
            
            for childNode in valueAsList:
                if hasattr(childNode, 'type') and type(childNode.type) is str:
                    traverse(childNode, visitor)
            
        visitor(node)
