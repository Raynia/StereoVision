def TupleAdd(t1, t2):
    result = []
    for index, value in enumerate(t1):
        result.append(value + t2[index])
    return tuple(result)