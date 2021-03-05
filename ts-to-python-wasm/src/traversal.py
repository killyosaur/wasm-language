from models.node import Node

def Traverse(nodes, visitor: callable):
    if type(nodes) is not list:
        nodes = [nodes]

    for node in nodes:
        print(node.type)
        for property, value in vars(node).items():
            valueAsList = value
            if type(value) is not list:
                valueAsList = [value]
            
            for childNode in valueAsList:
                print(childNode)
                if hasattr(childNode, 'type') and type(childNode.type) is str:
                    print(f'{childNode.type}')
                    Traverse(childNode, visitor)
            
        visitor(node)
