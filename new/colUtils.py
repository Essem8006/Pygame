def mixCol(a,b,percent):
    a = list(a)
    b = list(b)
    for i in range(3):
        a[i] += percent * (b[i]-a[i])
        a[i] = min(255,max(0,a[i]))
    return tuple(a)

def gradient(a,b,segments):
    cols = []
    for i in range(segments):
        cols.append(mixCol(a,b,i/(segments-1)))
    return cols