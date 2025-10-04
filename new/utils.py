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

def changingGradient(grad,y,segments):
    top_start = grad[0][0]
    bottom_start = grad[0][1]
    start = 0
    for top,bottom,when in grad:
        if y < when:
            diff = (y-start)/(when-start)
            return gradient(mixCol(top_start,top,diff),mixCol(bottom_start,bottom,diff),segments)
        else:
            top_start = top
            bottom_start = bottom
            start = when
    return gradient(top_start,bottom_start,segments)


def getMountains(width,height):
    """(0,134),
        (0,129),
        (13,126),
        (27,118),
        (43,114),
        (59,106),
        (73,115),
        (80,114),
        (91,121),
        (98,120),
        (115,131),
        (135,121),
        (143,125),
        (161,116),
        (177,103),#peak2
        (202,112),
        (214,109),
        (224,115),
        (224,134)"""
    template = [[#1
        (0,134),
        (0,129),
        (13,126),
        (27,118),
        (18,134)
    ],[#back
        (115,131),
        (121,132),
        (138,130),#need later
        (166,119),
        (177,103),#peak
        (161,116),
        (143,125),
        (135,121)
    ],[#4
        (113,134),
        (95,127),
        (89,127),
        (71,115),
        (80,114),
        (91,121),
        (98,120),
        (115,131),
        (121,132),
        (138,130),#need later
        (166,119),
        (177,103),#peak
        (178,115),
        (165,126),
        (186,115),
        (191,117),
        (163,132),
        (152,130),
        (138,134)
    ],[#2
        (27,118),
        (18,134),
        (95,134),
        (76,123),
        (59,120),
        (62,108),
        (59,106),
        (43,114)
    ],[#3
        (95,134),
        (76,123),
        (59,120),
        (62,108),
        (59,106),
        (113,134)
    ],[#for right
        (177,103),#peak
        (178,115),
        (165,126),
        (186,115),
        (191,117),
        (163,132),
        (152,130),
        (138,134),
        (224,134),
        (224,115),
        (214,109),
        (202,112)
    ]]
    points = []
    for temp in template:
        section = []
        for x,y in temp:
            section.append((x*width/224,y*height/134))
        points.append(section)
    return points