# get influence with distance
import math
closeness_that_matters = 100

def influence(dist):#0 -> 1
    return math.pow(max(0, closeness_that_matters - dist), 3) / (closeness_that_matters**3)

# get density
def density(particles, x, y):
    this_density = 0
    for part in particles:
        this_distance = math.sqrt( (part.pos[0] - x)**2 + (part.pos[1] - y)**2 )
        this_influence = influence(this_distance)
        this_density += this_influence
    return this_density


# get density decreasing gradient
def gradient(particles, pos):
    delta = 1 # because this is a set distance once a particle is closer than this they form a group
    subset = []
    for part in particles:
        this_distance = math.sqrt( (part.pos[0] - pos[0])**2 + (part.pos[1] - pos[1])**2 )
        if this_distance < closeness_that_matters:
            subset.append(part)
    neg_x = density(subset, pos[0] - delta, pos[1])
    pos_x = density(subset, pos[0] + delta, pos[1])
    neg_y = density(subset, pos[0], pos[1] - delta)
    pos_y = density(subset, pos[0], pos[1] + delta)
    return [neg_x - pos_x, neg_y - pos_y]