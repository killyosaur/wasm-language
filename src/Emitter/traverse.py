def Traverse(nodes, visitor):
    if isinstance(nodes, list) != True:
        nodes = [nodes]
    
    for node in nodes:
        for property, value in vars(node).items():
            valueAsArray = value
            if isinstance(value, list) != True:
                valueAsArray.append(value)
            for child in valueAsArray:
                Traverse(child, visitor)
        visitor(node)
