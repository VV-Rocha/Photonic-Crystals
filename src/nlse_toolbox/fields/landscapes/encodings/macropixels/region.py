import numpy as np


def feature_macropixel(mesh, size):
    width_px = len(np.where((mesh.x>-size[0]/2) * (mesh.x<size[0]/2))[0])
    height_px = len(np.where((mesh.y>-size[1]/2) * (mesh.y<size[1]/2))[0])
    
    feature = np.zeros((width_px, height_px), dtype=np.complex128)
    return feature