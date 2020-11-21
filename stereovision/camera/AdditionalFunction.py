def TupleAdd(t1, t2):
    result = []
    for index, value in enumerate(t1):
        result.append(value + t2[index])
    return tuple(result)

def SortTopBottomPoint(p1, p2):
    x1,x2,y1,y2 = 0,0,0,0
    x_sorted = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
    y_sorted = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])
    return (x_sorted[0], y_sorted[0]),(x_sorted[1], y_sorted[1])