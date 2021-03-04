def Traverse(nodes, visitor: callable):
    for node in nodes:
        for property, value in vars(node).items():
            valueAsList = value
            if type(value) is not list:
                valueAsList = [value]
            
            for childNode in valueAsList:
                if type(childNode.type) is str:
                    Traverse(childNode, visitor)
            
        visitor(node)
