import arrayfire as af


def from_numpy_to_arrayfire(arr):
    return af.from_ndarray(arr)

def from_arrayfire_to_numpy(arr):
    return arr.to_ndarray()