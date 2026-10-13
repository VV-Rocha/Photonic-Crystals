import numpy as np

from .square._square_lattice_vector_search import _square_lattice_vectors
from .rectangular._rectangular_lattice_vector_search import _rectangular_lattice_vectors



def find_moire_lattice_vectors(
    moire_config,
    print_err = True,
):
    if (moire_config["type"]=="rectangular"):
        a, error, periodic, theta_app = _rectangular_lattice_vectors(
            moire_config = moire_config,
            regime = "rational" if (moire_config["type"]=="square") else moire_config["regime"],
            max_denominator = moire_config["max_denominator"] if ("max_denominator" in moire_config.keys()) else 1000,
        )
    elif (moire_config["type"]=="square"):
        a, error, periodic, theta_app = _square_lattice_vectors(
            moire_config = moire_config,
        )
    
    if print_err:
        print("Angle error =", error)
        
    return np.array(a, dtype=float).reshape(-1, 2), error, periodic, theta_app