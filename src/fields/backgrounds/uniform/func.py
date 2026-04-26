import numpy as np


def uniform_field(I, shape):
    canvas = np.ones(shape, dtype=np.complex128)
    return np.sqrt(I) * canvas