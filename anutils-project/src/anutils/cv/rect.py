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

def image_box(img):
    iy,ix = img.shape[:2]
    tl = np.array([0,0])
    br = np.array([ix,iy])
    return (tl, br)

def bounding_box(points):
    tl = points.min(axis=0)
    br = points.max(axis=0)
    return (tl, br)

def box_dimensions(tl, br):
    return np.ceil(br - tl).astype(np.int32)