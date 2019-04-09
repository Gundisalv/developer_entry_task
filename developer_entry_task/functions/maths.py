import numpy as np


def min_dist_line(points):
    points = sorted(points)
    pair = sorted((points[0][1], points[1][1]))
    min_diff = abs(points[0][0]-points[1][0])
    for i in range(len(points)-1):
        if abs(points[i][0]-points[i+1][0]) < min_diff:
            pair = sorted((points[i][1], points[i+1][1]))
            min_diff = abs(points[i][0]-points[i+1][0])
    return pair


def min_dist_plane(points_c1, points_c2):
    pairs = list(zip(points_c1, points_c2))
    pairs_c1 = sorted(pairs, key=lambda x: x[0])
    pairs_c2 = sorted(pairs, key=lambda x: x[1])
    value_pair = closest_pair(pairs_c1, pairs_c2)
    return value_pair[:2]


def closest_pair(pairs_c1, pairs_c2):
    ln_pairs_c1 = len(pairs_c1)
    if ln_pairs_c1 <= 3:
        return min_dist_plane_small(pairs_c1)
    mid = ln_pairs_c1 // 2
    Qx = pairs_c1[:mid]
    Rx = pairs_c1[mid:]

    midpoint = pairs_c1[mid][0]
    Qy = list()
    Ry = list()
    for x in pairs_c2:
        if x[0] <= midpoint:
            Qy.append(x)
        else:
            Ry.append(x)

    # Call recursively both arrays after split
    (p1, q1, mi1) = closest_pair(Qx, Qy)
    (p2, q2, mi2) = closest_pair(Rx, Ry)

    # Determine smaller distance between points of 2 arrays
    if mi1 <= mi2:
        d = mi1
        mn = (p1, q1)
    else:
        d = mi2
        mn = (p2, q2)
    # Call function to account for points on the boundary
    (p3, q3, mi3) = closest_split_pair(pairs_c1, pairs_c2, d, mn)
    # Determine smallest distance for the array
    if d <= mi3:
        return mn[0], mn[1], d
    else:
        return p3, q3, mi3


def closest_split_pair(p_x, p_y, delta, best_pair):
    ln_x = len(p_x)
    mx_x = p_x[ln_x // 2][0]
    # Create a subarray of points not further than delta from
    # midpoint on x-sorted array
    s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
    best = delta  # assign best value to delta
    ln_y = len(s_y)  # store length of subarray for quickness
    for i in range(ln_y - 1):
        for j in range(i+1, min(i + 7, ln_y)):
            p, q = s_y[i], s_y[j]
            dst = dist(p, q)
            if dst < best:
                best_pair = p, q
                best = dst
    return best_pair[0], best_pair[1], best


def min_dist_plane_small(pairs_c1):
    mi = dist(pairs_c1[0], pairs_c1[1])
    p1 = pairs_c1[0]
    p2 = pairs_c1[1]
    ln_ax = len(pairs_c1)
    if ln_ax == 2:
        return p1, p2, mi
    for i in range(ln_ax-1):
        for j in range(i + 1, ln_ax):
            if i != 0 and j != 1:
                d = dist(pairs_c1[i], pairs_c1[j])
                if d < mi:  # Update min_dist and points
                    mi = d
                    p1, p2 = pairs_c1[i], pairs_c1[j]
    return p1, p2, mi


def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
