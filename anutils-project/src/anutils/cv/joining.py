import numpy as np

def intersects(a, b):
    return np.all((a > 0) & (b > 0), axis=2)

def union_box(box_1, box_2):
    tl1, br1 = box_1
    tl2, br2 = box_2
    tl_un = np.fmin(tl1, tl2)
    br_un = np.fmax(br1, br2)
    return (tl_un, br_un)

def union_image(img1, img0):
    rescale = np.ones(img1.shape[:2], np.uint8)
    rescale += np.where(intersects(img0, img1), np.uint8(1), np.uint8(0))
    rescale = rescale[:,:,np.newaxis]
    stitched = np.array([img0, img1], dtype=np.int16)
    return (stitched.sum(axis=0) // rescale).astype(np.uint8)