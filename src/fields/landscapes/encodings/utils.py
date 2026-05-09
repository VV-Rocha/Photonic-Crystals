import numpy as np


def size_tuple(func):
    def wrapper(size, n_features):
        if type(size)==float:
            size = (size, size)
        return func(size, n_features)
    return wrapper


@size_tuple
def _macropixel_size(size, n_features):
    Lx, Ly = size

    cols = np.ceil(np.sqrt(n_features))
    rows = np.ceil(n_features / cols)

    dx = Lx / cols
    dy = Ly / rows

    return (dx, dy)
        

def _encoding(encodings, n):
    if (type(encodings)==str):
        return {f"f{i}": encodings for i in range(n)}
    elif (type(encodings)==list):
        return {f"f{i}": encodings[i] for i in range(n)}