import numpy as np

def lattice_sum(
    xx_rot0,
    yy_rot0,
    xx_rot1,
    yy_rot1,
    a,
    p,
    lattice_function
    ):
    l_ = p[0] * lattice_function(xx_rot0, yy_rot0, a)
    l_ += p[1] * lattice_function(xx_rot1, yy_rot1, a)
        
    l_ /= np.max(np.abs(l_))
        
    return l_