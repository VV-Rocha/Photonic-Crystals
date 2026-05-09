import numpy as np

from .region import feature_macropixel


def clean_region(func):
    def wrapper(f, region):
        region *= 0.
        return func(f, region)
    return wrapper

@clean_region
def phase_encoding(f, region):
    region += 1.
    region *= np.exp(1.j * 2*np.pi * f)
    return region

@clean_region
def amplitude_encoding(f, region):
    region += f
    return region