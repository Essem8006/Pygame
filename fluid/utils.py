# get influence with distance
import math
import numpy as np
closeness_that_matters = 70
delta = 1

def distanceHelper(A, Bx, By):
    return math.sqrt( (A[0] - Bx)**2 + (A[1] - By)**2 )

# get density
def density(particles, x, y):
    # Extract positions into NumPy arrays
    px = np.array([p.pos[0] for p in particles])
    py = np.array([p.pos[1] for p in particles])
    
    # Vectorized distances
    dx = px - x
    dy = py - y
    dists = np.sqrt(dx * dx + dy * dy)
    influence_pre_cube = np.maximum(0.0, closeness_that_matters - dists)
    return np.sum((influence_pre_cube ** 3) / closeness_that_matters ** 3)


"""
# get density decreasing gradient
def gradient(particles, pos):
    subset = []
    for part in particles:
        this_distance = math.sqrt( (part.pos[0] - pos[0])**2 + (part.pos[1] - pos[1])**2 )
        if this_distance < closeness_that_matters:
            subset.append(part)
    neg_x = density(subset, pos[0] - delta, pos[1])
    pos_x = density(subset, pos[0] + delta, pos[1])
    neg_y = density(subset, pos[0], pos[1] - delta)
    pos_y = density(subset, pos[0], pos[1] + delta)
    return [neg_x - pos_x, neg_y - pos_y]"""

def gradient(particles, pos):
    """
    Compute approximate density gradient at 'pos' by finite differences.
    Optimized with vectorization and subset selection.
    """
    px = np.array([p.pos[0] for p in particles])
    py = np.array([p.pos[1] for p in particles])

    # Limit to nearby particles (within CLOSE + delta)
    dx_all = px - pos[0]
    dy_all = py - pos[1]
    dists_all = np.sqrt(dx_all * dx_all + dy_all * dy_all)
    nearby = dists_all < (closeness_that_matters + delta)
    px = px[nearby]
    py = py[nearby]

    # Compute four offset positions in one pass
    offsets = np.array([
        [-delta,  0],  # neg_x
        [ delta,  0],  # pos_x
        [ 0, -delta],  # neg_y
        [ 0,  delta]   # pos_y
    ])
    densities = np.zeros(4)

    for i, (ox, oy) in enumerate(offsets):
        dx = px - (pos[0] + ox)
        dy = py - (pos[1] + oy)
        dists = np.sqrt(dx * dx + dy * dy)
        influence = np.maximum(0.0, closeness_that_matters - dists)
        densities[i] = np.sum((influence ** 3) / closeness_that_matters ** 3)

    # Return density gradient
    return np.array([densities[0] - densities[1], densities[2] - densities[3]])