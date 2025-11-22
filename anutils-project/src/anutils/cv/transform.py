import numpy as np

def homogenize(p, axes=None):
    """
    Convert row matrix of points to homogenous coordinates
    """
    return np.vstack((p.T, np.ones((1,p.shape[0]))))

def unhomogenize(h):
    """
    Convert homogenous coordinates to row matrix of points
    """
    return (h / h[2:,:]).T[:,:2]

def transform(points, M):
    h_points = homogenize(points)
    h_trns_points = M @ h_points
    trns_points = unhomogenize(h_trns_points)
    return trns_points

def translation(p):
    return np.array([
        [1,0,p[0]],
        [0,1,p[1]],
        [0,0,1]
    ])

identity = np.array([
    [1,0,0],
    [0,1,0],
    [0,0,1]
])