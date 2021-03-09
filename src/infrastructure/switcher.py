def switch(argument, dictionary: dict, default):
    result = dictionary.get(argument, default)

    if callable(result):
        return result()
    else:
        return result
