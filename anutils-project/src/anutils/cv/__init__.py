import numpy as np



def rect(w, h, tr=(0,0)):
    tr = np.array([*tr])
    sizes = np.array([[w,h]])
    return tr + rects(sizes)[0,:,:]


def rects(sizes):
    rect_indeces = [[0,0],[1,0],[1,2],[0,2]]
    zeros = np.zeros((sizes.shape[0],1))
    sizes_exp = np.concatenate((zeros, sizes), axis=1)
    return sizes_exp[:,rect_indeces]
    

def homogenize(p, axes=None):
    return np.vstack((
        p.T, np.ones((1,p.shape[0]))
    ))

def homogenize_1d(p):
    return np.concatenate((p, np.array([1])))

def unhomogenize(h):
    return (h / h[2:,:]).T[:,:2]

def unhomogenize_1d(h):
    return h[:2] / h[2]