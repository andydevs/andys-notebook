import numpy as np



def rect(w, h, tr=(0,0)):
    tr = np.array([*tr])
    return tr + np.array([
        [ 0, 0 ],
        [ w, 0 ],
        [ w, h ],
        [ h, 0 ]
    ])


def homogenize(p):
    return np.vstack((
        p.T, np.ones((1,p.shape[0]))
    ))

def unhomogenize(h):
    return (h / h[2:,:]).T[:,:2]