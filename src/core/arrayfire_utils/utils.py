import arrayfire as af

from .decorators import scalar_to_list

def from_numpy_to_arrayfire(arr):
    return af.from_ndarray(arr)

def from_arrayfire_to_numpy(arr):
    return arr.to_ndarray()

class NpConversionMethods:
    @scalar_to_list
    def np_to_af(self, arr):
        return from_numpy_to_arrayfire(arr)
    
    def af_to_np(self, arr):
        return from_arrayfire_to_numpy(arr)